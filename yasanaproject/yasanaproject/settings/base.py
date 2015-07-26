

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

WEB_ROOT_DIR = os.path.dirname(BASE_DIR)  # this contains other folders like static and virtualenv e.t.c.


def generate_secret_key():
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(50))

SECRET_KEY = '8e9abs-c2enlkzbfqb%^^ancduyy2fthxh#$12=^jefck=2&=o'

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'yasana',
    'account',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'yasanaproject.urls'

WSGI_APPLICATION = 'yasanaproject.wsgi.application'


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

# noinspection PyUnresolvedReferences
STATIC_ROOT = os.path.join(WEB_ROOT_DIR, "static")

TEMPLATE_DIRS = (os.path.join(BASE_DIR,  'templates'),)

SESSION_COOKIE_NAME = 'asana_seskie'

SESSION_COOKIE_SECURE = True
#
SESSION_ENGINE = 'django.contrib.sessions.backends.cached_db'


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.db.DatabaseCache',
        'LOCATION': 'django_cache',
        'TIMEOUT': 60,
        'OPTIONS': {
            'MAX_ENTRIES': 1000,
            'CULL_FREQUENCY': 4,
        },

        'KEY_PREFIX': 'yasana'
    },

    'memcached': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
        'TIMEOUT': 60,
        'KEY_PREFIX': 'yasana'
    },

    'memcached_unix_socket': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': 'unix:/tmp/memcached.socket',
        'TIMEOUT': 60,
        'KEY_PREFIX': 'yasana'
    }
}

AUTH_USER_MODEL = 'yasana.UserProfile'

