from django.urls import path

from .views import (
    RfidListCreate,
    RfidRetrieveUpdateDestroy,
    CardDestroy,
    CardListCreate,
)

urlpatterns = [
    path("", RfidListCreate.as_view()),
    path("<int:pk>/", RfidRetrieveUpdateDestroy.as_view()),
    path("card/", CardListCreate.as_view()),
    path("card/<int:pk>/", CardDestroy.as_view()),
]
