from .base import *
from datetime import timedelta

DEBUG = False
ALLOWED_HOSTS = ["*"]
SECRET_KEY = "PxnYV_PyxyJNbp7pODS2CjXe1CL0j-YcN0E5KWk5HUQ6-Us37MIm4U12QnbqXNpMHe0"

# Database
BASE_DIR = Path(__file__).resolve().parent.parent

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": ":memory:",
    }
}

# Celery
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = "Europe/Warsaw"

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {"hosts": ["redis://localhost:6379/1"]},
    },
}

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(seconds=100000),
    "REFRESH_TOKEN_LIFETIME": timedelta(seconds=100000),
    "ROTATE_REFRESH_TOKENS": False,
}
