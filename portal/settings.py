# -*- coding: utf-8 -*-
"""
Django settings for portal project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys
from decouple import config
from dj_database_url import parse as db_url

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = ['.localhost', '127.0.0.1', '10.0.0.30', '.ifmt.edu.br']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'gunicorn',
    'filer',
    'mptt',
    'easy_thumbnails',
    'haystack',
    'whoosh',
    'reversion',
    'taggit',
    'taggit_autosuggest',
    'pure_pagination',
    'embed_video',
    'django_extensions',
    'adminsortable',

    'portal.autorizacao',
    'portal.banner',
    'portal.conteudo',
    'portal.core',
    'portal.cursos',
    'portal.menu',
    'portal.dirf',
)

MIDDLEWARE_CLASSES = (
    'portal.middlewares.UrlMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware',
)

ROOT_URLCONF = 'portal.urls'

WSGI_APPLICATION = 'portal.wsgi.application'

REMOVE_WWW = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': config(
        'DATABASE_URL',
        default='sqlite:///' + os.path.join(BASE_DIR + '/db.sqlite3'),
        cast=db_url),
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'pt-br'

LANGUAGES = (
    ('pt-br', u'Português'),
)

LOCALE_PATHS = (BASE_DIR + '/locale',)

TIME_ZONE = 'America/Cuiaba'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR + '/staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR + '/media')

SITE_ID = 1

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

TESTING = 'test' in sys.argv

from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
    'portal.core.context_processors.carregar_site_e_menus',
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR + '/portal/templates'),
)

if config('LDAP_ACTIVE', default=False):

    AUTHENTICATION_BACKENDS = (
        'portal.ldapauth.LDAPBackend',
        'django.contrib.auth.backends.ModelBackend',
    )

    # ldap settings for ldap backend
    import ldap

    LDAP_DEBUG = True
    LDAP_SERVER_URI = config('LDAP_SERVER_URI', default='')
    LDAP_PREBINDDN = config('LDAP_PREBINDDN', default='')
    LDAP_PREBINDPW = config('LDAP_PREBINDPW', default='')
    LDAP_SEARCHDN = config('LDAP_SEARCHDN', default='')
    LDAP_SEARCH_FILTER = 'cn=%s'  # or sAMAccountName
    LDAP_SCOPE = ldap.SCOPE_SUBTREE
    LDAP_UPDATE_FIELDS = True

    # Required unless LDAP_FULL_NAME is set:
    LDAP_FIRST_NAME = 'givenName'
    LDAP_LAST_NAME = 'sn'

    # Optional Settings:
    LDAP_FULL_NAME = 'displayName'
    # LDAP_GID -- string, LDAP attribute to get group name/number from
    # LDAP_SU_GIDS -- list of strings, group names/numbers that are superusers
    # LDAP_STAFF_GIDS -- list of strings, group names/numbers that are staff
    LDAP_EMAIL = 'mail'

MIGRATION_MODULES = {
    'filer': 'filer.migrations_django',
}

# Utilizado para testes
FILER_PUBLIC = os.path.join(BASE_DIR + '/filer_public')
FILER_PUBLIC_THUMBNAIL = os.path.join(BASE_DIR + '/filer_public_thumbnails/filer_public')

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

MPTT_ADMIN_LEVEL_INDENT = 20

WHOOSH_INDEX = os.path.join(BASE_DIR + '/whoosh')

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_INDEX,
    },
}

PAGINATION_SETTINGS = {
    'PAGE_RANGE_DISPLAYED': 6,
    'MARGIN_PAGES_DISPLAYED': 2,
}

CACHE_ACTIVE = config('CACHE_ACTIVE', default=False, cast=bool)

if CACHE_ACTIVE and not TESTING:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
            'LOCATION': config('CACHE_LOCATION'),
            'TIMEOUT': config('CACHE_TIMEOUT', default=500, cast=int),
        },
    }
else:  # Assume development mode
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }

CACHE_MIDDLEWARE_SECONDS = config('CACHE_MIDDLEWARE_SECONDS', default=180, cast=int)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'log_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filters': ['require_debug_false'],
            'filename': os.path.join(BASE_DIR, 'logs/django.log'),
            'when': 'W5',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['log_file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}
