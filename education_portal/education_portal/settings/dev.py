from .base import *
import os
import environ

env = environ.Env(DEBUG=(bool, True))
env_file = os.path.join(BASE_DIR, ".env")
environ.Env.read_env(env_file)

DEV_DEBUG = env('DEV_DEBUG')
DEV_SECRET_KEY = env('DEV_SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = DEV_DEBUG

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = DEV_SECRET_KEY

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

cwd = os.getcwd()
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": f"{cwd}/.cache"
    }
}

try:
    from .local import *
except ImportError:
    pass
