from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from django.utils import timezone
from utils.get_model_serializer_by_fun import get_model_serializer_by_fun
from event.serializer import EventSerializer

from ..models import (
    Device,
)


class DeviceSerializer(ModelSerializer):
    is_favourite = serializers.SerializerMethodField()
    # is_online = serializers.SerializerMethodField()

    class Meta:
        model = Device
        exclude = [
            "port",
            "mac",
        ]
        read_only_fields = ["ip", "last_seen"]

    # def get_is_online(self, obj: Device):
    #     return obj.last_seen > timezone.now() - timezone.timedelta(minutes=10)

    def get_is_favourite(self, obj: Device):
        if not obj.room:
            return False
        return obj.room.user.favourite.device.filter(pk=obj.pk).exists()

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        model_class, serializer_class = self._get_device_serializer(instance)
        serializer = serializer_class(
            model_class.objects.get(pk=instance.id), context=self.context
        )
        data = serializer.data

        data["events"] = EventSerializer(instance.events.all(), many=True).data
        representation.update(data)
        return representation

    def update(self, instance, validated_data):
        model_class, serializer_class = self._get_device_serializer(instance)
        serializer = serializer_class(
            model_class.objects.get(pk=instance.id),
            data=self.initial_data,
            context=self.context,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return instance

    def create(self, validated_data):
        model_class, serializer_class = self._get_device_serializer(validated_data)
        serializer = serializer_class(data=self.initial_data, context=self.context)
        serializer.is_valid(raise_exception=True)
        return serializer.save()

    def _get_device_serializer(self, obj: Device):
        fun: str = obj.fun.lower()
        if not fun:
            raise serializers.ValidationError("Pole 'fun' jest wymagane.")
        model_class, serializer_class = get_model_serializer_by_fun(fun)
        if not serializer_class:
            raise serializers.ValidationError(f"Nieobsługiwany typ urządzenia: {fun}")
        return model_class, serializer_class
