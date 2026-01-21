from .base import *

SECRET_KEY = "unsafe-dev-secret-key"
DEBUG = True
ALLOWED_HOSTS = []

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": str(BASE_DIR / 'db.sqlite3'),  # must be string
    }
}