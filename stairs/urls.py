from django.urls import path
from .views import RetrieveUpdateDestroyStairs

urlpatterns = [
    path(
        "<pk>/",
        RetrieveUpdateDestroyStairs.as_view(),
        name="retrieve-update-destroy-stairs",
    ),
]
