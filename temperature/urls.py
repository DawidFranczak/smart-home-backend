from django.urls import path

from .views import TempHumList, TempHumRetrieveUpdate

urlpatterns = [
    path("", TempHumList.as_view(), name="temp-hum-list"),
    path("<pk>/", TempHumRetrieveUpdate.as_view(), name="temp-hum-retrieve"),
]
