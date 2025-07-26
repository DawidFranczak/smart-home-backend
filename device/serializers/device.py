from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from device_registry import DeviceRegistry
from event.serializer import EventSerializer
from utils.web_socket_message import update_frontend_device

from ..models import (
    Device,
)


class DeviceSerializer(ModelSerializer):
    is_favourite = serializers.SerializerMethodField()

    class Meta:
        model = Device
        exclude = [
            "port",
            "mac",
        ]
        read_only_fields = ["ip", "last_seen"]

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
        update_frontend_device(instance, 200)
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
        register = DeviceRegistry()
        model_class = register.get_model(fun)
        serializer_class = register.get_serializer(fun)
        if not serializer_class:
            raise serializers.ValidationError(f"Nieobsługiwany typ urządzenia: {fun}")
        return model_class, serializer_class
