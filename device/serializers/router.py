from rest_framework import serializers
from django.utils import timezone
from ..models import Router, Device


class RouterSerializer(serializers.ModelSerializer):
    connected_devices = serializers.SerializerMethodField()
    online_device = serializers.SerializerMethodField()

    class Meta:
        model = Router
        fields = "__all__"

    def get_connected_devices(self, obj: Router):
        return Device.objects.filter(room__home=obj.home).count()

    def get_online_device(self, obj: Router):
        return Device.objects.filter(
            room__home=obj.home,
            is_online=True,
        ).count()

    def validate_mac(self, value):
        if len(value) < 1:
            raise serializers.ValidationError("MAC cannot be empty")
        if Router.objects.filter(mac=value).exists():
            raise serializers.ValidationError("Router already exists")
        return value
