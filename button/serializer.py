from rest_framework import serializers

from consumers.router_message.message_event import MessageEvent
from utils.delete_events_on_button_type_change import (
    delete_events_on_button_type_change,
)
from .models import Button, ButtonType
from device.models import Event


class ButtonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Button
        exclude = ["mac"]

    def validate_button_type(self, value):
        if value not in [ButtonType.MONOSTABLE, ButtonType.BISTABLE]:
            raise serializers.ValidationError("Wrong button type")
        return value

    def update(self, instance: Button, validated_data: dict):
        if "button_type" in validated_data:
            delete_events_on_button_type_change(validated_data["button_type"], instance)
        return super().update(instance, validated_data)


class ButtonSerializerDevice(serializers.ModelSerializer):

    class Meta:
        model = Button
        fields = ["name", "button_type"]
