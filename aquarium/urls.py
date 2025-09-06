from django.urls import path

from .views import *

urlpatterns = [
    path("", AquariumList.as_view()),
    path("<pk>/", AquariumRetrieveUpdateDestroy.as_view()),
]
