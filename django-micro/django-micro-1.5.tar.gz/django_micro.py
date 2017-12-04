from importlib import import_module
import inspect
import sys
import os

import django
from django.conf import settings
from django.core import management
from django.template import Library
from django.urls import path, re_path
from django.core.management.base import BaseCommand
from django.core.exceptions import ImproperlyConfigured

__all__ = ['command', 'configure', 'run', 'route', 'template', 'get_app_label']

register = template = Library()
urlpatterns = []

_app_module = None
_app_label = None
_commands = {}


def _create_app(stack):
    # extract directory, filename and app label from parent module
    app_module = sys.modules[stack[1][0].f_locals['__name__']]
    app_dirname = os.path.dirname(os.path.abspath(app_module.__file__))
    app_file_name = os.path.basename(app_module.__file__).split('.')[0]
    app_label = os.path.basename(app_dirname)

    app_module_name = '{}.{}'.format(app_label, app_file_name)

    # use parent directory of application as import root
    sys.path[0] = os.path.dirname(app_dirname)

    # allow relative import from app.py
    app_module.__package__ = app_label
    import_module(app_label)

    if app_module.__name__ != app_module_name:
        # allow recursive import app.py
        sys.modules[app_module_name] = app_module

    globals().update(_app_module=app_module, _app_label=app_label)


def get_app_label():
    if not _app_label:
        raise ImproperlyConfigured(
            "Application label is not detected. "
            "Check whether the configure() was called.")
    return _app_label


def route(pattern, view_func=None, regex=False, *args, **kwargs):
    path_func = re_path if regex else path

    def decorator(view_func):
        if hasattr(view_func, 'as_view'):
            view_func = view_func.as_view()

        urlpatterns.append(path_func(pattern, view_func, *args, **kwargs))
        return view_func

    # allow use decorator directly
    # route('blog/', show_index)
    if view_func:
        return decorator(view_func)

    return decorator


def configure(config_dict={}):
    _create_app(inspect.stack())  # load application from parent module

    if 'BASE_DIR' in config_dict:
        config_dict.setdefault('TEMPLATE_DIRS', [os.path.join(config_dict['BASE_DIR'], 'templates')])

    kwargs = {
        'INSTALLED_APPS': [_app_label] + config_dict.pop('INSTALLED_APPS', []),
        'ROOT_URLCONF': __name__,
        'TEMPLATES': [{
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': config_dict.pop('TEMPLATE_DIRS', []),
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': config_dict.pop('CONTEXT_PROCESSORS', []),
                'builtins': [__name__],
            },
        }],
    }

    kwargs.update({key: val for key, val in config_dict.items() if key.isupper()})
    settings.configure(**kwargs)
    django.setup()


def _patch_get_commands():
    django_get_commands = management.get_commands

    def patched_get_commands():
        commands = django_get_commands()
        commands.update(_commands)
        return commands

    patched_get_commands.patched = True
    management.get_commands = patched_get_commands


def command(name=None, command_cls=None):
    if not getattr(management.get_commands, 'patched', False):
        _patch_get_commands()

    if inspect.isfunction(name):
        # Shift arguments if decroator called without brackets
        command_cls = name
        name = None

    def decorator(command_cls):
        command_name = name

        if inspect.isclass(command_cls):
            command_instance = command_cls()
        else:
            # transform function-based command to class
            command_name = name or command_cls.__name__
            command_instance = type('Command', (BaseCommand,), {'handle': command_cls})()

        if not command_name:
            raise DjangoMicroException("Class-based commands requires name argument.")

        # Hack for extracting app name from command (https://goo.gl/1c1Irj)
        command_instance.rpartition = lambda x: [_app_label]

        _commands[command_name] = command_instance
        return command_cls

    # allow use decorator directly
    # command('print_hello', PrintHelloCommand)
    if command_cls:
        return decorator(command_cls)

    return decorator


class DjangoMicroException(Exception):
    pass


def run():
    if not settings.configured:
        raise ImproperlyConfigured("You should call configure() after configuration define.")

    if _app_module.__name__ == '__main__':
        from django.core.management import execute_from_command_line
        execute_from_command_line(sys.argv)
    else:
        from django.core.wsgi import get_wsgi_application
        return get_wsgi_application()
