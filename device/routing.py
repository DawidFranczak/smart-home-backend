from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(
        r"ws/router/(?P<mac_address>[0-9A-Fa-f:]+)/$",
        consumers.RouterConsumer.as_asgi(),
    ),
]
