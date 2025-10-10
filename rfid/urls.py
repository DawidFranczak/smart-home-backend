from django.urls import path

from .views import (
    RfidListCreate,
    RfidRetrieveUpdateDestroy,
    CardDestroy,
    CardListCreate,
)

urlpatterns = [
    path("", RfidListCreate.as_view(), name="rfid-list-create"),
    path("<int:pk>/", RfidRetrieveUpdateDestroy.as_view()),
    path("card/", CardListCreate.as_view(), name="card-list-create"),
    path("card/<int:pk>/", CardDestroy.as_view(), name="card-destroy"),
]
