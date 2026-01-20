from django.db import models
from device.models import Device


class Stairs(Device):
    brightness = models.SmallIntegerField(default=100)
    step = models.SmallIntegerField(default=100)
    lighting_time = models.SmallIntegerField(default=10)
    light_count = models.IntegerField(default=16)
