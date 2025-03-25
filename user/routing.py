from django.urls import path
from .consumer import UserConsumer

websocket_urlpatterns = [path(r"ws/user/<str:token>/", UserConsumer.as_asgi())]
