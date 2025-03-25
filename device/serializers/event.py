from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from ..models import (
    Event,
)


class EventSerializer(ModelSerializer):
    device = serializers.SerializerMethodField()

    def get_device(self, object):
        return object.device.name

    class Meta:
        model = Event
        exclude: list[str] = ["id"]
