from rest_framework import serializers

from consumers.router_message.builders.basic import set_settings_request
from consumers.router_message.messenger import DeviceMessenger
from .models import Lamp


class LampSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lamp
        exclude = ["mac"]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        data = LampSerializerDevice(instance).data
        request = set_settings_request(instance.mac, data)
        DeviceMessenger().send(instance.get_router_mac(), request)
        return instance


class LampSerializerDevice(serializers.ModelSerializer):
    class Meta:
        model = Lamp
        fields = ["brightness", "step", "lighting_time"]
