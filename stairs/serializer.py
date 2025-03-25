from rest_framework import serializers
from django.utils import timezone

from .models import Stairs


class StairsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Stairs
        exclude = ["fun", "id", "port", "wifi_strength", "mac"]
