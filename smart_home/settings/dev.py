from .base import *
from corsheaders.defaults import default_headers

DEBUG = True
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY")
SITE_DOMAIN = "http://192.168.1.116"
FIRMWARE_DEVICE_ENDPOINT = SITE_DOMAIN + "/api/firmware/download/"
CORS_ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://192.168.1.142:5173",
    "https://halpiszony.dpdns.org",
]
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:5173",
    "http://192.168.1.142:5173",
    "https://halpiszony.dpdns.org",
]
ALLOWED_HOSTS = ["*"]
CORS_ALLOW_CREDENTIALS = True

CORS_ALLOW_HEADERS = list(default_headers) + [
    "ngrok-skip-browser-warning",
]
