from .base import *
from corsheaders.defaults import default_headers

DEBUG = True
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")

CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
]
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "ngrok-skip-browser-warning",
]