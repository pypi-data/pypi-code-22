# Default Django settings. Override these with settings in the module
# pointed-to by the DJANGO_SETTINGS_MODULE environment variable.

# This is defined here as a do-nothing function because we can't import
# django.utils.translation -- that module depends on the settings.
gettext_noop = lambda s: s
####################
# CORE             #
####################

DEBUG = False
TEMPLATE_DEBUG = False


# Whether the framework should propagate raw exceptions rather than catching
# them. This is useful under some testing situations and should never be used
# on a live site.
DEBUG_PROPAGATE_EXCEPTIONS = False

# Whether to use the "Etag" header. This saves bandwidth but slows down performance.
USE_ETAGS = False

# People who get code error notifications.
# In the format [('Full Name', 'email@example.com'), ('Full Name', 'anotheremail@example.com')]
ADMINS = []


# Local time zone for this installation. All choices can be found here:
# https://en.wikipedia.org/wiki/List_of_tz_zones_by_name (although not all
# systems may support all possibilities). When USE_TZ is True, this is
# interpreted as the default user time zone.
TIME_ZONE = 'Asiz/Shanghai'

# If you set this to True, Django will use timezone-aware datetimes.
USE_TZ = False

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'


# Not-necessarily-technical managers of the site. They get broken link
# notifications and other various emails.
MANAGERS = ADMINS

# Default content type and charset to use for all HttpResponse objects, if a
# MIME type isn't manually specified. These are used to construct the
# Content-Type header.
DEFAULT_CONTENT_TYPE = 'text/html'
DEFAULT_CHARSET = 'utf-8'

# Encoding of files read from disk (template and initial SQL files).
FILE_CHARSET = 'utf-8'

# Email address that error messages come from.
SERVER_EMAIL = 'root@localhost'

# Database connection info. If left empty, will default to the dummy backend.
DATABASES = {}

# Classes used to implement DB routing behavior.
DATABASE_ROUTERS = []

# The email backend to use. For possible shortcuts see django.core.mail.
# The default is to use the SMTP backend.
# Third-party backends can be specified by providing a Python path
# to a module that defines an EmailBackend class.
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host for sending email.
EMAIL_HOST = 'localhost'

# Port for sending email.
EMAIL_PORT = 25

# Optional SMTP authentication information for EMAIL_HOST.
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''
EMAIL_USE_TLS = False
EMAIL_USE_SSL = False
EMAIL_SSL_CERTFILE = None
EMAIL_SSL_KEYFILE = None
EMAIL_TIMEOUT = None

# List of strings representing installed apps.
INSTALLED_APPS = []

# List of strings representing apps to output to logs.
LOGGING_APPS = []

# List of locations of the template source files, in search order.
TEMPLATE_DIRS = []

# List of callables that know how to import templates from various sources.
# See the comments in django/core/template/loader.py for interface
# documentation.
TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]

# List of processors used by RequestContext to populate the context.
# Each one should be a callable that takes the request object as its
# only parameter and returns a dictionary to add to the context.
TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    # 'django.template.context_processors.request',
    'django.contrib.messages.context_processors.messages',
]

# Output to use in template system for invalid (e.g. misspelled) variables.
TEMPLATE_STRING_IF_INVALID = ''

TEMPLATES = []

# Default email address to use for various automated correspondence from
# the site managers.
DEFAULT_FROM_EMAIL = 'webmaster@localhost'

# Subject-line prefix for email messages send with django.core.mail.mail_admins
# or ...mail_managers.  Make sure to include the trailing space.
EMAIL_SUBJECT_PREFIX = '[Moose] '

# Whether to append trailing slashes to URLs.
APPEND_SLASH = True

# Whether to prepend the "www." subdomain to URLs that don't have it.
PREPEND_WWW = False

# Override the server-derived value of SCRIPT_NAME
FORCE_SCRIPT_NAME = None

# List of compiled regular expression objects representing User-Agent strings
# that are not allowed to visit any page, systemwide. Use this for bad
# robots/crawlers. Here are a few examples:
#     import re
#     DISALLOWED_USER_AGENTS = [
#         re.compile(r'^NaverBot.*'),
#         re.compile(r'^EmailSiphon.*'),
#         re.compile(r'^SiteSucker.*'),
#         re.compile(r'^sohu-search')
#     ]
DISALLOWED_USER_AGENTS = []

ABSOLUTE_URL_OVERRIDES = {}

# List of strings representing allowed prefixes for the {% ssi %} tag.
# Example: ['/home/html', '/var/www']
ALLOWED_INCLUDE_ROOTS = []

# List of compiled regular expression objects representing URLs that need not
# be reported by BrokenLinkEmailsMiddleware. Here are a few examples:
#    import re
#    IGNORABLE_404_URLS = [
#        re.compile(r'^/apple-touch-icon.*\.png$'),
#        re.compile(r'^/favicon.ico$),
#        re.compile(r'^/robots.txt$),
#        re.compile(r'^/phpmyadmin/),
#        re.compile(r'\.(cgi|php|pl)$'),
#    ]
IGNORABLE_404_URLS = []

# A secret key for this particular Django installation. Used in secret-key
# hashing algorithms. Set this in your settings, or Django will complain
# loudly.
SECRET_KEY = ''

# Default file storage mechanism that holds media.
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = None

# URL that handles the static files served from STATIC_ROOT.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = None

# List of upload handler classes to be applied in order.
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]


# Default formatting for date objects. See all available format strings here:
# http://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
DATE_FORMAT = 'N j, Y'

# Default formatting for datetime objects. See all available format strings here:
# http://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
DATETIME_FORMAT = 'N j, Y, P'

# Default formatting for time objects. See all available format strings here:
# http://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
TIME_FORMAT = 'P'

# Default formatting for date objects when only the year and month are relevant.
# See all available format strings here:
# http://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
YEAR_MONTH_FORMAT = 'F Y'

# Default formatting for date objects when only the month and day are relevant.
# See all available format strings here:
# http://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
MONTH_DAY_FORMAT = 'F j'

# Default short formatting for date objects. See all available format strings here:
# http://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
SHORT_DATE_FORMAT = 'm/d/Y'

# Default short formatting for datetime objects.
# See all available format strings here:
# http://docs.djangoproject.com/en/dev/ref/templates/builtins/#date
SHORT_DATETIME_FORMAT = 'm/d/Y P'

# Default formats to be used when parsing dates from input boxes, in order
# See all available format string here:
# http://docs.python.org/library/datetime.html#strftime-behavior
# * Note that these format strings are different from the ones to display dates
DATE_INPUT_FORMATS = [
    '%Y-%m-%d', '%m/%d/%Y', '%m/%d/%y',  # '2006-10-25', '10/25/2006', '10/25/06'
    '%b %d %Y', '%b %d, %Y',             # 'Oct 25 2006', 'Oct 25, 2006'
    '%d %b %Y', '%d %b, %Y',             # '25 Oct 2006', '25 Oct, 2006'
    '%B %d %Y', '%B %d, %Y',             # 'October 25 2006', 'October 25, 2006'
    '%d %B %Y', '%d %B, %Y',             # '25 October 2006', '25 October, 2006'
]

# Default formats to be used when parsing times from input boxes, in order
# See all available format string here:
# http://docs.python.org/library/datetime.html#strftime-behavior
# * Note that these format strings are different from the ones to display dates
TIME_INPUT_FORMATS = [
    '%H:%M:%S',     # '14:30:59'
    '%H:%M:%S.%f',  # '14:30:59.000200'
    '%H:%M',        # '14:30'
]

# Default formats to be used when parsing dates and times from input boxes,
# in order
# See all available format string here:
# http://docs.python.org/library/datetime.html#strftime-behavior
# * Note that these format strings are different from the ones to display dates
DATETIME_INPUT_FORMATS = [
    '%Y-%m-%d %H:%M:%S',     # '2006-10-25 14:30:59'
    '%Y-%m-%d %H:%M:%S.%f',  # '2006-10-25 14:30:59.000200'
    '%Y-%m-%d %H:%M',        # '2006-10-25 14:30'
    '%Y-%m-%d',              # '2006-10-25'
    '%m/%d/%Y %H:%M:%S',     # '10/25/2006 14:30:59'
    '%m/%d/%Y %H:%M:%S.%f',  # '10/25/2006 14:30:59.000200'
    '%m/%d/%Y %H:%M',        # '10/25/2006 14:30'
    '%m/%d/%Y',              # '10/25/2006'
    '%m/%d/%y %H:%M:%S',     # '10/25/06 14:30:59'
    '%m/%d/%y %H:%M:%S.%f',  # '10/25/06 14:30:59.000200'
    '%m/%d/%y %H:%M',        # '10/25/06 14:30'
    '%m/%d/%y',              # '10/25/06'
]

# First day of week, to be used on calendars
# 0 means Sunday, 1 means Monday...
FIRST_DAY_OF_WEEK = 0

# Decimal separator symbol
DECIMAL_SEPARATOR = '.'

# Boolean that sets whether to add thousand separator when formatting numbers
USE_THOUSAND_SEPARATOR = False

# Number of digits that will be together, when splitting them by
# THOUSAND_SEPARATOR. 0 means no grouping, 3 means splitting by thousands...
NUMBER_GROUPING = 0

# Thousand separator symbol
THOUSAND_SEPARATOR = ','

# The tablespaces to use for each model when not specified otherwise.
DEFAULT_TABLESPACE = ''
DEFAULT_INDEX_TABLESPACE = ''

# The Python dotted path to the WSGI application that Django's internal server
# (runserver) will use. If `None`, the return value of
# 'django.core.wsgi.get_wsgi_application' is used, thus preserving the same
# behavior as previous versions of Django. Otherwise this should point to an
# actual WSGI application object.
WSGI_APPLICATION = None

# If your Django app is behind a proxy that sets a header to specify secure
# connections, AND that proxy ensures that user-submitted headers with the
# same name are ignored (so that people can't spoof it), set this value to
# a tuple of (header_name, header_value). For any requests that come in with
# that header/value, request.is_secure() will return True.
# WARNING! Only set this if you fully understand what you're doing. Otherwise,
# you may be opening yourself up to a security risk.
SECURE_PROXY_SSL_HEADER = None

##############
# MIDDLEWARE #
##############

# List of middleware classes to use.  Order is important; in the request phase,
# this middleware classes will be applied in the order given, and in the
# response phase the middleware will be applied in reverse order.
MIDDLEWARE_CLASSES = [

]

############
# SESSIONS #
############

# Cache to store session data if using the cache session backend.
SESSION_CACHE_ALIAS = 'default'
# Cookie name. This can be whatever you want.
SESSION_COOKIE_NAME = 'sessionid'
# Age of cookie, in seconds (default: 2 weeks).
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7 * 2
# A string like ".example.com", or None for standard domain cookie.
SESSION_COOKIE_DOMAIN = None
# Whether the session cookie should be secure (https:// only).
SESSION_COOKIE_SECURE = False
# The path of the session cookie.
SESSION_COOKIE_PATH = '/'
# Whether to use the non-RFC standard httpOnly flag (IE, FF3+, others)
SESSION_COOKIE_HTTPONLY = True
# Whether to save the session data on every request.
SESSION_SAVE_EVERY_REQUEST = False
# Whether a user's session cookie expires when the Web browser is closed.
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
# The module to store session data
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
# Directory to store session files if using the file session module. If None,
# the backend will use a sensible default.
SESSION_FILE_PATH = None
# class to serialize session data
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

#########
# CACHE #
#########

# The cache backends to use.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
    }
}
CACHE_MIDDLEWARE_KEY_PREFIX = ''
CACHE_MIDDLEWARE_SECONDS = 600
CACHE_MIDDLEWARE_ALIAS = 'default'


###########
# SIGNING #
###########

SIGNING_BACKEND = 'django.core.signing.TimestampSigner'


############
# MESSAGES #
############

# Class to use as messages backend
MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

# Default values of MESSAGE_LEVEL and MESSAGE_TAGS are defined within
# django.contrib.messages to avoid imports in this settings file.

###########
# LOGGING #
###########

# The callable to use to configure logging
LOGGING_CONFIG = 'logging.config.dictConfig'

# Custom logging configuration.
LOGGING = {}

# Default exception reporter filter class used in case none has been
# specifically assigned to the HttpRequest instance.
DEFAULT_EXCEPTION_REPORTER_FILTER = 'django.views.debug.SafeExceptionReporterFilter'

###########
# TESTING #
###########

# The name of the class to use to run the test suite
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Apps that don't need to be serialized at test database creation time
# (only apps with migrations are to start with)
TEST_NON_SERIALIZED_APPS = []


###########
# LOGGING #
###########
