from django.urls import path
from .views import GetActionsAndEvents, GetDeviceByFunction, CreateDeleteEvent

urlpatterns = [
    path("", GetActionsAndEvents.as_view()),
    path("<int:pk>/", CreateDeleteEvent.as_view()),
    path("action/", GetDeviceByFunction.as_view()),
]
