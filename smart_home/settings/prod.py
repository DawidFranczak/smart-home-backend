import os
from corsheaders.defaults import default_headers

from .base import *

DEBUG = False
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

CORS_ALLOWED_ORIGINS = [
    "https://dashing-cod-pretty.ngrok-free.app",
    "https://halpiszony.share.zrok.io",
]
CSRF_TRUSTED_ORIGINS = [
    "https://dashing-cod-pretty.ngrok-free.app",
    "https://halpiszony.share.zrok.io",
]
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "ngrok-skip-browser-warning",
]
