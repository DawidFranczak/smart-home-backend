from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated

from camera.serializer import CameraReadSerializer,CameraWriteSerializer
from .models import Camera

from django.shortcuts import get_list_or_404

class ListCreateCameraView(ListCreateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CameraWriteSerializer
        return CameraReadSerializer

    def get_queryset(self):
        return get_list_or_404(Camera, home__users=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data["home"] = request.user.home.first().id
        print(request.data)
        return super().create(request, *args, **kwargs)