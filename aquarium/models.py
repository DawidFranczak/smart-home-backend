from django.db import models
from django.utils import timezone
from device.models import Device


class Aquarium(Device):
    color_r = models.SmallIntegerField(default=255)
    color_g = models.SmallIntegerField(default=255)
    color_b = models.SmallIntegerField(default=255)
    led_start = models.TimeField(default=timezone.now)
    led_stop = models.TimeField(default=timezone.now)
    fluo_start = models.TimeField(default=timezone.now)
    fluo_stop = models.TimeField(default=timezone.now)
    mode = models.BooleanField(default=False)
    led_mode = models.BooleanField(default=False)
    fluo_mode = models.BooleanField(default=False)
