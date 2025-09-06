from django.contrib import admin
from django.urls import path, include, re_path
from user.views import index
from user.views import index

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", index, name="index"),
    path("api/", include("user.urls")),
    path("api/room/", include("room.urls")),
    path("api/lamp/", include("lamp.urls")),
    path("api/device/", include("device.urls")),
    path("api/aquarium/", include("aquarium.urls")),
    path("api/button/", include("button.urls")),
    path("api/rfid/", include("rfid.urls")),
    path("api/event/", include("event.urls")),
    path("api/cameras/", include("camera.urls")),
    re_path(r"^.*$", index),
]
