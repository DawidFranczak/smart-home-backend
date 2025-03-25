from django.db import models
from device.models import Device


# Create your models here.
class Stairs(Device):
    steps = models.IntegerField(default=200)
    brightness = models.IntegerField(default=100)
    light_time = models.IntegerField(default=6)
    mode = models.BooleanField(default=False)
