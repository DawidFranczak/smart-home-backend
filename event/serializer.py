from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from device.models import (
    Event,
)


class EventSerializer(ModelSerializer):
    device = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = "__all__"

    def get_device(self, obj: Event):
        return f"{obj.target_device.room.name}-{obj.target_device.name}"
