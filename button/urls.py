from django.urls import path

from .views import ButtonListAPIView, ButtonRetrieveUpdateDestroy

urlpatterns = [
    path("", ButtonListAPIView.as_view(), name="button-list"),
    path(
        "<int:pk>/",
        ButtonRetrieveUpdateDestroy.as_view(),
        name="button-retrieve-update-destroy",
    ),
]
