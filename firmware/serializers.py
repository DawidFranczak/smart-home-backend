from rest_framework import serializers

from firmware.models import FirmwareDevice


class FirmwareDeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = FirmwareDevice
        fields = ["to_device", "version"]
