from django.urls import path
from .views import LampGetAll, RetrieveUpdateDestroyLamp

urlpatterns = [
    path("", LampGetAll.as_view(), name="get-lamp"),
    path(
        "<pk>/",
        RetrieveUpdateDestroyLamp.as_view(),
        name="retrieve-update-destroy-lamp",
    ),
]
