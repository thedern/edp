import os
from .base import *
import environ

env = environ.Env(DEBUG=(bool, False))
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)

# False if not in os.environ
DEBUG = env('DEBUG')
SECRET_KEY = env("SECRET_KEY")
DB_PASS = env('DB_PASS')
DB_USER = env('DB_USER')
DB_NAME = env('DB_NAME')

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
        "NAME": DB_NAME,
        "USER": DB_USER,
        "PASSWORD": DB_PASS,
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
