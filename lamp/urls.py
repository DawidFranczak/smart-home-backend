from django.urls import path
from .views import LampGetAll, RetrieveUpdateDestroyLamp, LampToggleLight

urlpatterns = [
    path("", LampGetAll.as_view()),
    path("<pk>/", RetrieveUpdateDestroyLamp.as_view()),
    path("<pk>/toggle/", LampToggleLight.as_view()),
]
