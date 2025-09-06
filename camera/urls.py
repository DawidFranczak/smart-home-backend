from django.urls import path

from camera.views import ListCreateCameraView

urlpatterns = [
    path('cameras/', ListCreateCameraView.as_view(), name='camera-list-create'),
]