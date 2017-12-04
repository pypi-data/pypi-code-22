"""
Modis Lock
-----

Modis Lock Description Here

````````````
Code Example:
.. code:: python
    from modis_admin_app import create_app

    app = create_app()

    if __name__ == "__main__":
        app.run()

`````````````````
And run it:
.. code:: bash
    $ pip install Flask
    $ python hello.py
    * Running on http://localhost:5000/
Ready for production? `Read this first <http://flask.pocoo.org/docs/deploying/>`.
Links
`````
* `website <http://flask.pocoo.org/>`_
* `documentation <http://flask.pocoo.org/docs/>`_
* `development version
  <https://github.com/pallets/flask/zipball/master#egg=Flask-dev>`_
"""

# Setuptools
from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from sphinx.setup_command import BuildDoc

# Subprocessing
from subprocess import check_call

# Libraries
#from distutils.sysconfig import get_python_lib
import site

# Misc
from shutil import chown
import os
import sys


if sys.version_info < (3, 5):
    raise Exception("Modis Lock requires Python 3.5 or higher.")

with open('./README.rst', encoding='utf-8') as f:
    readme = f.read()


def _get_requirements():
    """Returns all requirements for the modules

    :return:
    """
    return [i.strip() for i in open("./requirements.txt").readlines()]


class PostDevelopCommand(develop):
    """Develop command for setuptools

    """
    def run(self):
        # TODO Post install script here or call a function
        develop.run(self)


class PostInstallCommand(install):
    """Install command for setuptools

    """
    pre_args = ['apt', 'install', '-y', 'libsystemd-dev', 'libffi-dev', 'python3-pkgconfig', 'libssl-dev']
    key_args = ['openssl', 'genrsa', '-out', '/var/www/modislock.key', '2048']
    cert_args = ['openssl', 'req', '-new', '-x509', '-key', '/var/www/modislock.key', '-out', '/var/www/modislock.cert',
                 '-days', '3650', '-subj']
    install_dir = None
    hostname = None

    def _build_assets(self):
        os.chdir(self.install_dir)
        from modislock_webservice.extensions import asset_bundles
        from webassets import Environment

        os.chdir(self.install_dir)
        env = Environment(directory=self.install_dir + '/static', url='/static')

        for key in asset_bundles.keys():
            env.register(key, asset_bundles[key])
            env[key].urls()

    def _build_documentation(self):
        pass

    def _pre_install(self):
        # Install OS dependencies
        check_call(self.pre_args)

    def _post_install(self):
        # Create a symbolic link for the web server to find the static files

        if os.path.islink('/var/www/modislock'):
            os.remove('/var/www/modislock')
        os.symlink(self.install_dir, '/var/www/modislock', target_is_directory=True)

        # Generate the key
        check_call(self.key_args)

        # Generate certificate
        self.cert_args.append('/CN=' + self.hostname + '.local')
        check_call(self.cert_args)

        self._build_assets()
        self._build_documentation()

        # Permissions
        for r, d, f in os.walk(self.install_dir + '/pages'):
            chown(r, user='root', group='www-data')
            os.chmod(r, 0o755)

        for r, d, f in os.walk(self.install_dir + '/static'):
            chown(r, user='root', group='www-data')
            os.chmod(r, 0o755)

    def run(self):
        # Generate the certificate
        with open('/etc/hostname', 'r') as f:
            self.hostname = f.readline().rstrip()

        self.install_dir = site.getsitepackages()[0] + '/modislock_webservice'
        # Pre-install
        self._pre_install()
        # Install
        install.run(self)
        # Post-install
        self._post_install()


setup(
    name='modislock',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.1.1',

    description='Administration web interface for Modis© Lock',
    long_description=readme,

    # The project's main homepage.
    url='https://github.com/Modis-GmbH/ModisLock-WebAdmin',

    # Choose your license
    license='GPL',

    # Author details
    author='Richard Lowe',
    author_email='richard@modislab.com',

    # What does your project relate to?
    keywords=['modis', 'raspberry pi', 'lock', 'administration'],

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Environment :: Console",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: POSIX :: Linux",
        "Topic :: Security"
    ],

    platforms=['Linux', 'Raspberry Pi'],

    zip_safe=False,

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(exclude=['docs', 'tests*']),

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=_get_requirements(),

    # If your project only runs on certain Python versions, setting the python_requires argument to the appropriate
    # PEP 440 version specifier string will prevent pip from installing the project on other Python versions.
    python_requires='>=3.5',

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    include_package_data=True,

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    data_files=[('/etc/supervisor/conf.d', ['deploy/modis_admin.conf']),
                ('/etc/profile.d', ['deploy/flask_env.sh']),
                ('/etc/nginx/sites-available', ['deploy/admin_site']),
                ('/etc/nginx/sites-available', ['deploy/supervisord_site'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={
        'console_scripts': [
            'modis_admin = modislock_webservice.wsgi:main',
            'modis_admin_worker = modislock_webservice.celery_worker:main'
        ]
    },

    cmdclass={'develop': PostDevelopCommand,
              'install': PostInstallCommand,
              'build_sphinx': BuildDoc}
)
