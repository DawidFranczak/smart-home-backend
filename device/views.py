from django.shortcuts import get_list_or_404, get_object_or_404

from rest_framework.response import Response
from rest_framework.generics import (
    ListCreateAPIView,
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
)
from rest_framework.permissions import IsAuthenticated

from device.models import Device, Router
from room.models import Room
from utils.get_model_serializer_by_fun import get_model_serializer_by_fun
from .serializers.device import DeviceSerializer
from .serializers.router import RouterSerializer


class ListCreateRouter(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = RouterSerializer

    def get_queryset(self):
        return get_list_or_404(Router, home__users=self.request.user)

    def create(self, request, *args, **kwargs):
        request.data["home"] = request.user.home.all().first().id
        return super().create(request, *args, **kwargs)


class ListCreateDevice(ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        if self.request.query_params.get("unassigned", False):
            return get_list_or_404(
                Device, home__users=self.request.user, room__isnull=True
            )
        elif "function" in self.request.query_params:
            fun = self.request.query_params.get("function")
            model, _ = get_model_serializer_by_fun(fun.lower())
            if not model:
                return Device.objects.none()
            return get_list_or_404(model, home__users=self.request.user)
        return Device.objects.filter(room__user=self.request.user)

    def create(self, request, *args, **kwargs):
        data = request.data
        room = get_object_or_404(Room, user=self.request.user, pk=data["room_id"])
        device = get_object_or_404(
            Device, home__users=self.request.user, pk=data["device_id"]
        )
        device.room = room
        device.save(update_fields=["room"])
        return Response(data, 201)


class RetrieveUpdateDestroyDevice(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return Device.objects.filter(home__users=self.request.user)

    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)
