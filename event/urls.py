from django.urls import path
from .views import GetActionsAndEvents

urlpatterns = [
    path("get/action/", GetActionsAndEvents.as_view()),
]
