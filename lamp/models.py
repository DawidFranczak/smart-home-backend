import datetime
from django.db import models
from device.models import Device


# Create your models here.
class Lamp(Device):
    light_start = models.TimeField(
        default=datetime.datetime.now().replace(second=0, microsecond=0)
    )
    light_stop = models.TimeField(
        default=datetime.datetime.now().replace(second=0, microsecond=0)
    )
    brightness = models.SmallIntegerField(default=100)
    step = models.SmallIntegerField(default=21)
    lighting_time = models.SmallIntegerField(default=10)
