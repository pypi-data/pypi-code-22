# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from distutils.version import LooseVersion
import warnings

import pytest
from selenium import __version__ as SELENIUM_VERSION
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options


def pytest_addoption(parser):
    group = parser.getgroup('selenium', 'selenium')
    group._addoption('--firefox-path',
                     metavar='path',
                     help='path to the firefox binary.')
    group._addoption('--firefox-preference',
                     action='append',
                     default=[],
                     dest='firefox_preferences',
                     metavar=('name', 'value'),
                     nargs=2,
                     help='additional firefox preferences.')
    group._addoption('--firefox-profile',
                     metavar='path',
                     help='path to the firefox profile.')
    group._addoption('--firefox-extension',
                     action='append',
                     default=[],
                     dest='firefox_extensions',
                     metavar='path',
                     help='path to a firefox extension.')


def pytest_configure(config):
    config.addinivalue_line(
        'markers', "firefox_arguments(args): arguments to be passed to "
        "Firefox. This marker will be ignored for other browsers. For "
        "example: firefox_arguments('-foreground')")
    config.addinivalue_line(
        'markers', "firefox_preferences(dict): preferences to be passed to "
        "Firefox. This marker will be ignored for other browsers. For "
        "example: firefox_preferences({'browser.startup.homepage': "
        "'https://pytest.org/'})")


def driver_kwargs(capabilities, driver_log, driver_path, firefox_options,
                  **kwargs):
    kwargs = {}
    if capabilities:
        kwargs['capabilities'] = capabilities
    if driver_log is not None:
        kwargs['log_path'] = driver_log
    if driver_path is not None:
        kwargs['executable_path'] = driver_path

    # Selenium 3.8.0 deprecated firefox_options in favour of options
    if LooseVersion(SELENIUM_VERSION) < LooseVersion('3.8.0'):
        kwargs['firefox_options'] = firefox_options
    else:
        kwargs['options'] = firefox_options
    return kwargs


@pytest.fixture
def firefox_options(request, firefox_path, firefox_profile):
    options = Options()

    if firefox_profile is not None:
        options.profile = firefox_profile

    if firefox_path is not None:
        options.binary = FirefoxBinary(firefox_path)

    args = request.node.get_marker('firefox_arguments')
    if args is not None:
        for arg in args.args:
            options.add_argument(arg)

    prefs = request.node.get_marker('firefox_preferences')
    if prefs is not None:
        for name, value in prefs.args[0].items():
            options.set_preference(name, value)

    return options


@pytest.fixture(scope='session')
def firefox_path(pytestconfig):
    if pytestconfig.getoption('firefox_path'):
        warnings.warn(
            '--firefox-path has been deprecated and will be removed in a '
            'future release. Please make sure the Firefox binary is in the '
            'default location, or the system path. If you want to specify a '
            'binary path then use the firefox_options fixture to and set this '
            'using firefox_options.binary.', DeprecationWarning)
        return pytestconfig.getoption('firefox_path')


@pytest.fixture
def firefox_profile(pytestconfig):
    profile = None
    if pytestconfig.getoption('firefox_profile'):
        profile = FirefoxProfile(pytestconfig.getoption('firefox_profile'))
        warnings.warn(
            '--firefox-profile has been deprecated and will be removed in '
            'a future release. Please use the firefox_options fixture to '
            'set a profile path or FirefoxProfile object using '
            'firefox_options.profile.', DeprecationWarning)
    if pytestconfig.getoption('firefox_preferences'):
        profile = profile or FirefoxProfile()
        warnings.warn(
            '--firefox-preference has been deprecated and will be removed in '
            'a future release. Please use the firefox_options fixture to set '
            'preferences using firefox_options.set_preference. If you are '
            'using Firefox 47 or earlier then you will need to create a '
            'FirefoxProfile object with preferences and set this using '
            'firefox_options.profile.', DeprecationWarning)
        for preference in pytestconfig.getoption('firefox_preferences'):
            name, value = preference
            if value.isdigit():
                # handle integer preferences
                value = int(value)
            elif value.lower() in ['true', 'false']:
                # handle boolean preferences
                value = value.lower() == 'true'
            profile.set_preference(name, value)
        profile.update_preferences()
    if pytestconfig.getoption('firefox_extensions'):
        profile = profile or FirefoxProfile()
        warnings.warn(
            '--firefox-extensions has been deprecated and will be removed in '
            'a future release. Please use the firefox_options fixture to '
            'create a FirefoxProfile object with extensions and set this '
            'using firefox_options.profile.', DeprecationWarning)
        for extension in pytestconfig.getoption('firefox_extensions'):
            profile.add_extension(extension)
    return profile
