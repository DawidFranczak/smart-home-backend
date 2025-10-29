from rest_framework import serializers

from consumers.router_message.builders.basic import set_settings_request
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.messenger import DeviceMessenger
from utils.sleeping_time import sleeping_time
from .models import TempHum


class TempHumSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempHum
        exclude = [
            "mac",
            "home",
        ]

    def update(self, instance, validated_data):
        super().update(instance, validated_data)
        request: DeviceMessage = set_settings_request(instance.mac, validated_data)
        DeviceMessenger().send(instance.get_router_mac(), request)
        return instance


class TempHumSerializerDevice(serializers.ModelSerializer):
    sleeping_time = serializers.SerializerMethodField()

    def get_sleeping_time(self, obj) -> int:
        return sleeping_time()

    class Meta:
        model = TempHum
        fields = ["sleeping_time"]
