from django.urls import path

from .views import TempHumList, TempHumRetrieve, TempHumHistoryView

urlpatterns = [
    path("", TempHumList.as_view(), name="temp-hum-list"),
    path("<pk>/", TempHumRetrieve.as_view(), name="temp-hum-retrieve"),
    path("history/<pk>/", TempHumHistoryView.as_view(), name="temp-hum-retrieve"),
]
