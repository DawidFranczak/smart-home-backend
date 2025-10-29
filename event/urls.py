from django.urls import path
from .views import (
    GetActionsAndEvents,
    GetAvailableActionAndExtraSettings,
    CreateDeleteEvent,
)

urlpatterns = [
    path("", GetActionsAndEvents.as_view()),
    path("<int:pk>/", CreateDeleteEvent.as_view()),
    path("action/", GetAvailableActionAndExtraSettings.as_view()),
]
