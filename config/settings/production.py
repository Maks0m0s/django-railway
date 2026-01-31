from .base import *

SECRET_KEY = os.environ.get(
    "SECRET_KEY",
    "django-insecure-DEV-FALLBACK-ONLY"
)

DEBUG = False

ROOT_URLCONF = "config.urls"

ALLOWED_HOSTS = [ '*' ]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("PGDATABASE"),
        "USER": os.environ.get("PGUSER"),
        "PASSWORD": os.environ.get("POSTGRES_PASSWORD"),
        "HOST": os.environ.get("PGHOST"),
        "PORT": os.environ.get("PGPORT"),
    }
}

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")