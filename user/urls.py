from django.urls import path
from django.urls.resolvers import URLPattern
from .views import (
    LogoutView,
    LoginView,
    RefreshAccessToken,
    RegisterView,
    FavouriteView,
)

urlpatterns: list[URLPattern] = [
    path("login/", LoginView.as_view()),
    path("registration/", RegisterView.as_view()),
    path("token/refresh/", RefreshAccessToken.as_view()),
    path("logout/", LogoutView.as_view()),
    path("favourite/", FavouriteView.as_view()),
]
