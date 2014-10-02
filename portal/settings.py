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
from unipath import Path
from dj_database_url import parse as db_url

BASE_DIR = Path(__file__).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

TEMPLATE_DEBUG = DEBUG

DEBUG_TOOLBAR_PATCH_SETTINGS = False

TESTING = 'test' in sys.argv

ADMINS = (('Equipe Sistemas', 'sistemas@ifmt.edu.br'), )

# Email config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = True

ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '200.129.244.17', '.herokuapp.com']


# Application definition

INSTALLED_APPS = (
    # Pre apps

    # Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # External apps
    'gunicorn',
    'devserver',
    'south',
    'mptt',
    'django_summernote',
    'filer',
    'easy_thumbnails',
    'taggit',
    'debug_toolbar',
    'django_extensions',
    'adminsortable',
    'haystack',
    'whoosh',
    'taggit_autosuggest',
    'reversion',

    # Project apps
    'portal.core',
    'portal.conteudo',
    'portal.banner',
    'portal.cursos',
    'portal.autorizacao',
)

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

SITE_ID = 1

# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + BASE_DIR.child('db.sqlite3'),
        cast=db_url),
}

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

# AUTH_USER_MODEL='core.User'

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Cuiaba'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

STATIC_ROOT = BASE_DIR.child('staticfiles')
STATIC_URL = '/static/'

MEDIA_ROOT = BASE_DIR.child('media')
MEDIA_URL = '/media/'

# Templates
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'portal.core.context_processors.carregar_site_e_menus',
)

# TEMPLATE_LOADERS = (
#     'django.template.loaders.filesystem.Loader',
#     'django.template.loaders.app_directories.Loader',
# )

TEMPLATE_DIRS = (
    BASE_DIR.child('portal').child('templates'),
)

WHOOSH_INDEX = BASE_DIR.child('whoosh')

# HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_INDEX,
    },
}

MPTT_ADMIN_LEVEL_INDENT = 20

# Utilizado para testes
FILER_PUBLIC = BASE_DIR.child('filer_public')
FILER_PUBLIC_THUMBNAIL = BASE_DIR.child('filer_public_thumbnails').child('filer_public')

# Habilita as permissoes do django-filer
FILER_ENABLE_PERMISSIONS = True

FILER_DUMP_PAYLOAD = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'easy_thumbnails.processors.scale_and_crop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

SOUTH_MIGRATION_MODULES = {
    'easy_thumbnails': 'easy_thumbnails.south_migrations',
    'taggit': 'taggit.south_migrations',
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
        # 'strikethrough', 'clear']],
        # ['para', ['ul', 'ol']],
        ['para', ['ul', 'ol', 'paragraph']],
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video']],
        ['misc', ['codeview']]
    ],
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        # Include the default Django email handler for errors
        'mail_admins': {
            'class': 'django.utils.log.AdminEmailHandler',
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
        # Log to a text file that can be rotated by logrotate
        'logfile': {
            'class': 'logging.handlers.WatchedFileHandler',
            'filename': BASE_DIR.child('logs').child('error.log'),
        },
    },
    'loggers': {
        # Again, default Django configuration to email unhandled exceptions
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        # Might as well log any errors anywhere else in Django
        'django': {
            'handlers': ['logfile'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
