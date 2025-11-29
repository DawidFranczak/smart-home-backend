from django.urls import path
from .views import (
    GetActionsAndEvents,
    GetAvailableActionAndExtraSettings,
    CreateDeleteEvent,
    TriggerEvent,
)

urlpatterns = [
    path("", GetActionsAndEvents.as_view(), name="actions-and-events"),
    path("<int:pk>/", CreateDeleteEvent.as_view(), name="event-create-delete"),
    path(
        "action/",
        GetAvailableActionAndExtraSettings.as_view(),
        name="available-actions",
    ),
    path("trigger/", TriggerEvent.as_view(), name="trigger-event"),
]
