from django.urls import path

from .views import ListCreateRoomView, RetrieveUpdateDestroyRoomView

urlpatterns = [
    path("", ListCreateRoomView.as_view(), name="room-list-create"),
    path(
        "<int:pk>/",
        RetrieveUpdateDestroyRoomView.as_view(),
        name="room-retrieve-update-destroy",
    ),
]
