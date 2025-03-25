from django.db import models
from device.models import Device


# Create your models here.
class TemperatureSensor(Device):
    time = models.DateTimeField(auto_now_add=False)
    value = models.FloatField()
    humi = models.FloatField(default="")
