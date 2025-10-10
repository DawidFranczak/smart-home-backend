from django.urls import re_path, path
from .router import RouterConsumer
from .frontend import UserConsumer
from .camera import CameraConsumer

websocket_urlpatterns = [
    re_path(r"ws/router/(?P<mac_address>[0-9A-Fa-f:]+)/$", RouterConsumer.as_asgi()),
    path(r"ws/user/<str:token>/", UserConsumer.as_asgi()),
    path(r"ws/camera/<str:token>/<int:pk>/", CameraConsumer.as_asgi()),
]
