from django.urls import path

from .views import *

urlpatterns = [
    path("", AquariumList.as_view(),name='aquarium-list'),
    path("<pk>/", AquariumRetrieveUpdateDestroy.as_view(),name='aquarium-retrieve-update-destroy'),
]
