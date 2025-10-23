from rest_framework import serializers

from utils.sleeping_time import sleeping_time
from .models import TempHum


class TempHumSerializer(serializers.ModelSerializer):
    class Meta:
        model = TempHum
        fields = "__all__"


class TempHumSerializerDevice(serializers.ModelSerializer):
    sleeping_time = serializers.SerializerMethodField()

    def get_sleeping_time(self, obj) -> int:
        return sleeping_time()

    class Meta:
        model = TempHum
        fields = ["sleeping_time"]
