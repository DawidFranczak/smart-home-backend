from django.utils import timezone
from rest_framework import serializers
from .models import Sunblind


class SunblindSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sunblind
        fields = "__all__"
