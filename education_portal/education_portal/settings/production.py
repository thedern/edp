import os
from .base import *

# all information in this file needs to be moved to .env file
DEBUG = False
SECRET_KEY = '&^kwxz2zf!x=%+358)i#^t(f@^fd%z0wfa5r$cm$^95-_m#z0!'
ALLOWED_HOSTS = ['localhost', 'linkece.com', '45.79.143.131']
cwd = os.getcwd()
CACHES = {
    "default": {
        "BACKEND": 'django.core.cache.backends.filebased.FileBasedCache',
        "LOCATION": f"{cwd}/.cache"
    }
}

DATABASES = {
    "default": {
        "ENGINE": 'django.db.backends.postgresql_psycopg2',
        "NAME": 'education_portal',
        "USER": 'edp_user',
        "PASSWORD": 'zrx1200r',
        "HOST": "localhost",
        "PORT": "",
    }
}

# sentry
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

sentry_sdk.init(
    dsn="https://72e0bc37b359428d8779a34bd331ebf1@sentry.io/3515687",
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

try:
    from .local import *
except ImportError:
    pass
