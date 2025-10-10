from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet

from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from device.serializers.device import DeviceSerializer
from .models import Aquarium


class AquariumList(ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        user: AbstractBaseUser | AnonymousUser = self.request.user
        return Aquarium.objects.filter(room__user=user)


class AquariumRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self) -> QuerySet[Aquarium, Aquarium]:
        return Aquarium.objects.filter(room__user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance: Aquarium = self.get_object()
        instance_data = self.get_serializer(instance).data
        diff_data = self._get_diff_data(request.data, instance_data)

        if not diff_data:
            return Response({}, status=200)

        serializer = self.get_serializer(instance, data=diff_data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({}, status=200)

    def _get_diff_data(self, new_data, instance_data):
        return {
            key: value
            for key, value in new_data.items()
            if key in instance_data and value != instance_data[key]
        }
