from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from camera.serializer import CameraSerializer
from .models import Camera

from django.shortcuts import get_list_or_404

class ListCreateCameraView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CameraSerializer

    def get_queryset(self):
        return get_list_or_404(Camera, home__users=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data["home"] = request.user.home.first().id
        return super().create(request, *args, **kwargs)