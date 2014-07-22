# coding: utf-8
"""
Django settings for portal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os
import sys
from decouple import config
from dj_database_url import parse as db_url
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
# BASE_DIR = os.path.dirname(os.path.abspath(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# configuracao para .env
try:
    execfile(os.path.join(BASE_DIR, '.env'))
except IOError:
    from django.utils.crypto import get_random_string
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    content = "SECRET_KEY='{}'\n".format(get_random_string(50, chars))
    content += 'DEBUG=False\n'
    content += 'SQL_LOG=False\n'
    open(os.path.join(BASE_DIR, '.env'), 'w').write(content)
    execfile(os.path.join(BASE_DIR, '.env'))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

TEMPLATE_DEBUG = DEBUG

TESTING = 'test' in sys.argv or not config('SQL_LOG', default=False, cast=bool)

ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '200.129.244.17', '.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    # External pre apps

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # External apps
    'south',
    'mptt',
    'django_summernote',
    'filer',
    'easy_thumbnails',

    # Project apps
    'portal.core',
    'portal.conteudo',
    'portal.banner',
    'portal.cursos',
)

if DEBUG:
    # Add here the debug apps
    DEBUG_APPS_BEFORE_INSTALLED_APPS = ()

    DEBUG_APPS = (
        'debug_toolbar',
        # 'django_nose',
        'django_extensions',
    )

    # Use nose to run all tests
    # TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    # Tell nose to measure coverage on the 'foo' and 'bar' apps

    # NOSE_ARGS = [
    #     '--with-coverage',
    #     '--cover-package=portal.core',
    #     '--nologcapture',
    # ]

    INSTALLED_APPS = DEBUG_APPS_BEFORE_INSTALLED_APPS + INSTALLED_APPS + DEBUG_APPS
else:
    # Add here the production apps
    PRODUCTION_APPS_BEFORE_INSTALLED_APPS = ()

    PRODUCTION_APPS = (
        'gunicorn',
    )

    INSTALLED_APPS = PRODUCTION_APPS_BEFORE_INSTALLED_APPS + INSTALLED_APPS + PRODUCTION_APPS

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'portal.urls'

WSGI_APPLICATION = 'portal.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + os.path.join(BASE_DIR, 'db.sqlite3'),
        cast=db_url),
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Cuiaba'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

FILER_PUBLIC = os.path.join(MEDIA_ROOT, 'filer_public')
FILER_PUBLIC_THUMBNAIL = os.path.join(MEDIA_ROOT, 'filer_public_thumbnails/filer_public')

# STATICFILES_DIRS = (
#     os.path.join(BASE_DIR, 'static'),
# )

# Usado pelo grappelli
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#     'django.contrib.staticfiles.finders.FileSystemFinder',
# )
#
# GRAPPELLI_ADMIN_TITLE = u'IFMT Portal - Administração'

# Usado pelo filebrowser
# DIRECTORY = os.path.join(MEDIA_ROOT, 'uploads/')

# Usando pelo django-filer
FILER_ENABLE_PERMISSIONS = True

FILER_DUMP_PAYLOAD = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    #'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
}

# Cache
CACHE_MIDDLEWARE_ANONYMOUS_ONLY = True

CACHE_ACTIVE = config('CACHE_ACTIVE', default=False, cast=bool)

if CACHE_ACTIVE:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
            'BINARY': True,
            'LOCATION': config('CACHE_LOCATION'),
            'OPTIONS': {
                'ketama': True,
                'tcp_nodelay': True,
            },
            'TIMEOUT': config('CACHE_TIMEOUT', default=500, cast=int),
        },
    }
else:  # Assume development mode
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }


# Templates
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += ('django.core.context_processors.request',)
# TEMPLATE_STRING_IF_INVALID = 'CONTEXT_ERROR'
TEMPLATE_DIRS = (
    os.path.join(os.path.dirname(__file__), 'templates'),
)


# Logging
def skip_on_testing(record):
    return not TESTING


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'normal': {
            'format': '%(levelname)s %(name)s %(message)s'
        },
        'sqlformatter': {
            '()': 'sqlformatter.SqlFormatter',
            'format': '%(levelname)s %(message)s',
        },
    },
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'skip_on_testing': {
            '()': 'django.utils.log.CallbackFilter',
            'callback': skip_on_testing,
        },
    },
    'handlers': {
        'stderr': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'normal',
            'filters': ['skip_on_testing'],
        },
        'sqlhandler': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'sqlformatter',
            'filters': ['require_debug_true', 'skip_on_testing'],
        },
    },
    'loggers': {
        'django.db.backends': {
            'handlers': ['sqlhandler'],
            'level': 'DEBUG',
        },
        'portal': {
            'handlers': ['stderr'],
            'level': 'INFO',
        },
    },
}

# Summernote configuration
SUMMERNOTE_CONFIG = {
    # Change editor size
    'width': '100%',

    # Set editor language/locale
    'lang': 'pt-BR',

    # Customize toolbar buttons
    'toolbar': [
        # ['style', ['style']],
        ['font', ['bold', 'italic', 'underline', 'clear']],
        # ['font', ['bold', 'italic', 'underline', 'superscript', 'subscript',
        #           'strikethrough', 'clear']],
        # ['para', ['ul', 'ol']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video']],
        ['misc', ['codeview']]
    ],

    # Set `upload_to` function for attachments.
    # 'attachment_upload_to': my_custom_upload_to_func(),

    # Set custom storage class for attachments.
    # 'attachment_storage_class': 'my.custom.storage.class.name',
}
