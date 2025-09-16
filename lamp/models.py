import datetime
from django.db import models
from device.models import Device
from enum import Enum


def default_time():
    return datetime.datetime.now().replace(second=0, microsecond=0).time()


class LampAction(Enum):
    ON = "on"
    OFF = "off"
    BLINK = "blink"
    TOGGLE = "toggle"


class Lamp(Device):
    light_start = models.TimeField(default=models.TimeField(default=default_time))
    light_stop = models.TimeField(default=models.TimeField(default=default_time))
    brightness = models.SmallIntegerField(default=100)
    step = models.SmallIntegerField(default=21)
    lighting_time = models.SmallIntegerField(default=10)

    @staticmethod
    def available_actions():
        return [action.value for action in LampAction]
