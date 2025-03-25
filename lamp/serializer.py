from rest_framework import serializers
from device.websocket_sender import send_data
from .models import Lamp

# class LampSerializer(ModelSerializer):

#     def update(self, instance, validated_data):
#         send_data(f"bs{validated_data["brightness"]}",instance.ip, instance.port)
#         send_data(f"sp{validated_data["step"]}",instance.ip, instance.port)
#         send_data(f"te{validated_data["lighting_time"]}",instance.ip, instance.port)
#         return super().update(instance, validated_data)

#     class Meta:
#         model = Lamp
#         exclude = ["fun","ip","port","user"]


class LampSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lamp
        exclude = [
            "port",
            "mac",
        ]

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        data = LampWebSocketSerializer(instance).data
        send_data(instance, data)
        return instance


class LampWebSocketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lamp
        fields = ["mac", "ip", "port", "brightness", "step", "lighting_time"]
