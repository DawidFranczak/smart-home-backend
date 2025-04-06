from django.utils import timezone
from rest_framework import serializers
from .models import Button


class ButtonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Button
        exclude = ["fun", "id", "port", "wifi_strength", "mac"]


class ButtonSerializerDevice(serializers.ModelSerializer):

    class Meta:
        model = Button
        fields = ["name"]
