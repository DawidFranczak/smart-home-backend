from django.db.models import QuerySet
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from device.serializers.device import DeviceSerializer
from .models import TempHum


class TempHumList(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self) -> QuerySet[TempHum, TempHum]:
        return TempHum.objects.filter(room__user=self.request.user)


class TempHumRetrieveUpdate(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DeviceSerializer

    def get_queryset(self) -> QuerySet[TempHum, TempHum]:
        return TempHum.objects.filter(room__user=self.request.user)
