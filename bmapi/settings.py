
# Django settings for bmapi project.

import os

DIRNAME = os.path.dirname(__file__)
_parent = lambda x: os.path.normpath(os.path.join(x, '..'))
PARENT_DIRNAME = _parent(DIRNAME)

ADMINS = (
    # ('Your Name', 'your_email@example.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'bmapi',                      # Or path to database file if using sqlite3.
        'USER': 'bmapi',                      # Not used with sqlite3.
        'PASSWORD': 'bmapi',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# On Unix systems, a value of None will cause Django to use the same
# timezone as the operating system.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/Los_Angeles'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

MEDIA_ROOT = os.path.join(DIRNAME, 'media')
STATIC_ROOT = os.path.join(DIRNAME, 'static')

MEDIA_URL = '/media/'
STATIC_URL = '/static/'

ADMIN_MEDIA_PREFIX = '/static/admin/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = ')n(*(bi71%1ty&c8)x*1!%8qmc1w5po@)!_8sd$jz&g9&n%*+d'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'playaevents.api.middleware.ContentTypeMiddleware',
    'playaevents.middleware.LoggedInMiddleware'
)

ROOT_URLCONF = 'bmapi.urls'

ACCOUNT_ACTIVATION_DAYS = 14
AUTH_PROFILE_MODULE = 'bmprofile.BmProfile'
LOGIN_REDIRECT_URL = '/'
LOGOUT_URL = '/'

TEMPLATE_DIRS = (
    os.path.join(PARENT_DIRNAME, "templates"),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django_extensions',
    'keyedcache',
    'registration',
    'bmprofile',
    'signedauth',
    'httpproxy',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

CACHE_LOCATION = os.path.join(PARENT_DIRNAME, 'cache')
if not os.path.exists(CACHE_LOCATION):
    os.mkdir(CACHE_LOCATION)

CACHES = {
    'default' : {
        'BACKEND' : 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION' : CACHE_LOCATION,
        'TIMEOUT' : 60*60*6 # 6 hours
        }
    }

CACHE_PREFIX = 'B'
CACHE_TIMEOUT = 60*60*24

DEBUG_TOOLBAR_CONFIG = { 'INTERCEPT_REDIRECTS': False }

LOGGED_IN_ONLY = False

PROXY_DOMAINS = {
    'playaevents' : {
        'server' : 'playaevents.burningman.com',
        },
    'mediagallery' : {
        'server' : 'gallery.burningman.com',
        }
}

from settings_local import *
