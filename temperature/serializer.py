from django.utils import timezone
from rest_framework import serializers
from .models import TemperatureSensor


class TemperatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemperatureSensor
        fields = "__all__"
