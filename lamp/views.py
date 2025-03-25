from kombu.asynchronous.http import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView

from device.serializers.device import DeviceSerializer
from .models import Lamp


class LampGetAll(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Lamp.objects.all()
    serializer_class = DeviceSerializer


class RetrieveUpdateDestroyLamp(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Lamp.objects.filter(room__user=self.request.user)


class LampToggleLight(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return Response(status=200)
