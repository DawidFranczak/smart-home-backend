from django.urls import path

from camera.views import ListCreateCameraView

urlpatterns = [
    path("", ListCreateCameraView.as_view(), name='camera-list-create'),
]