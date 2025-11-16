from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView

from device.serializers.device import DeviceSerializer
from .models import Button


class ButtonListAPIView(ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Button.objects.filter(room__user=self.request.user)


class ButtonRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Button.objects.filter(room__user=self.request.user)
