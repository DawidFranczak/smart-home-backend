import datetime
from django.db import models
from django.utils import timezone
from device.models import Device


class Aquarium(Device):
    color_r = models.SmallIntegerField(default=255)
    color_g = models.SmallIntegerField(default=255)
    color_b = models.SmallIntegerField(default=255)
    led_start = models.TimeField(
        default=datetime.datetime.now().replace(second=0, microsecond=0)
    )
    led_stop = models.TimeField(
        default=datetime.datetime.now().replace(second=0, microsecond=0)
    )
    fluo_start = models.TimeField(
        default=datetime.datetime.now().replace(second=0, microsecond=0)
    )
    fluo_stop = models.TimeField(
        default=datetime.datetime.now().replace(second=0, microsecond=0)
    )
    mode = models.BooleanField(default=False)
    led_mode = models.BooleanField(default=False)
    fluo_mode = models.BooleanField(default=False)
