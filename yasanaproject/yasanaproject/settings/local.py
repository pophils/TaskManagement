

from .base import *


DEBUG = True

TEMPLATE_DEBUG = True


INSTALLED_APPS += ("debug_toolbar",)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'django_db',
        'USER': 'django_user',
        'PASSWORD': 'adrianmoscow',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


MIDDLEWARE_CLASSES += (
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    )


SESSION_COOKIE_SECURE = False