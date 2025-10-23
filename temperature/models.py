from django.db import models
from device.models import Device
from django.utils import timezone


class TempHum(Device):
    battery_level = models.IntegerField(default=0)
    temperature = models.FloatField(default=None, blank=True, null=True)
    humidity = models.FloatField(default=None, blank=True, null=True)
    timestamp = models.DateTimeField(default=timezone.now)
