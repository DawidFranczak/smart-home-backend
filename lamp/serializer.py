from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework import serializers

from consumers.router_message.builders.basic import set_settings_request
from .models import Lamp


class LampSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lamp
        exclude = [
            "port",
            "mac",
        ]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        data = LampSerializerDevice(instance).data
        request = set_settings_request(instance.mac, data)
        async_to_sync(get_channel_layer().group_send)(
            f"router_{instance.get_router_mac()}",
            {"type": "router_send", "data": request.to_json()},
        )
        return instance


class LampSerializerDevice(serializers.ModelSerializer):
    class Meta:
        model = Lamp
        fields = ["brightness", "step", "lighting_time"]
