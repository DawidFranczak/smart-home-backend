import datetime
from django.db import models
from device.models import Device


def default_time():
    return datetime.datetime.now().replace(second=0, microsecond=0).time()


class Aquarium(Device):
    color_r = models.SmallIntegerField(default=255)
    color_g = models.SmallIntegerField(default=255)
    color_b = models.SmallIntegerField(default=255)
    led_start = models.TimeField(default=default_time)
    led_stop = models.TimeField(default=default_time)
    fluo_start = models.TimeField(default=default_time)
    fluo_stop = models.TimeField(default=default_time)
    mode = models.BooleanField(default=False)
    led_mode = models.BooleanField(default=False)
    fluo_mode = models.BooleanField(default=False)
