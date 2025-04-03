from django.urls import path
from .views import GetActionsAndEvents, GetDeviceByFunction, CreateEvent

urlpatterns = [
    path("", GetActionsAndEvents.as_view()),
    path("<int:pk>/", CreateEvent.as_view()),
    path("action/", GetDeviceByFunction.as_view()),
]
