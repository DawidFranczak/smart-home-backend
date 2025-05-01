from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser

from django.db.models.manager import BaseManager
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from device.serializers.device import DeviceSerializer
from .models import Aquarium


class AquariumGetAll(ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        user: AbstractBaseUser | AnonymousUser = self.request.user
        return Aquarium.objects.filter(room__user=user)


class AquariumRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self) -> BaseManager[Aquarium]:
        return Aquarium.objects.filter(room__user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance: Aquarium = self.get_object()
        instance_data = self.get_serializer(instance).data
        new_value = {}
        for key, value in request.data.items():
            if key in instance_data and value != instance_data[key]:
                new_value[key] = value

        if not new_value:
            return Response(self.get_serializer(instance).data)
        serializer = self.get_serializer(instance, data=new_value, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
