from django.urls import path
from .views import LampGetAll, RetrieveUpdateDestroyLamp

urlpatterns = [
    path("", LampGetAll.as_view()),
    path("<pk>/", RetrieveUpdateDestroyLamp.as_view()),
]
