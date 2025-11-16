from django.urls import path
from django.urls.resolvers import URLPattern
from device.views import (
    ListCreateDevice,
    ListCreateRouter,
    RetrieveUpdateDestroyDevice,
    UpdateButtonType,
)

urlpatterns: list[URLPattern] = [
    path("", ListCreateDevice.as_view()),
    path("<int:pk>/", RetrieveUpdateDestroyDevice.as_view()),
    path("router/", ListCreateRouter.as_view()),
    path("button-type/<pk>/", UpdateButtonType.as_view()),
]
