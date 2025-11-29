from django.db.models import QuerySet, Q

from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

from device.serializers.device import DeviceSerializer
from utils.get_available_for_user_device import get_available_for_user_device
from .models import Aquarium


class AquariumList(ListAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self):
        return get_available_for_user_device(Aquarium, self.request.user)


class AquariumRetrieveUpdateDestroy(RetrieveUpdateDestroyAPIView):
    serializer_class = DeviceSerializer

    def get_queryset(self) -> QuerySet[Aquarium, Aquarium]:
        return get_available_for_user_device(Aquarium, self.request.user)

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
