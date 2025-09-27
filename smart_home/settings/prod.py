import os
from corsheaders.defaults import default_headers

from .base import *

DEBUG = False
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

CORS_ALLOWED_ORIGINS = [
    "https://dashing-cod-pretty.ngrok-free.app",
]
CSRF_TRUSTED_ORIGINS = [
    "https://dashing-cod-pretty.ngrok-free.app",
]
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "ngrok-skip-browser-warning",
]

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRES_DB"),
        "USER": os.getenv("POSTGRES_USER"),
        "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
        "HOST": os.getenv("POSTGRES_HOST"),
        "PORT": os.getenv("POSTGRES_PORT"),
    }
}


# Celery
CELERY_BROKER_URL = os.getenv("REDIS_CELERY")
CELERY_RESULT_BACKEND = os.getenv("REDIS_CELERY")
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/Warsaw"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": [os.getenv("REDIS_CHANNEL_LAYERS")]},
    },
}


from datetime import timedelta


SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=int(os.getenv("ACCESS_TOKEN_LIFETIME"))),
    "REFRESH_TOKEN_LIFETIME": timedelta(
        seconds=int(os.getenv("REFRESH_TOKEN_LIFETIME"))
    ),
    "ROTATE_REFRESH_TOKENS": False,
}
