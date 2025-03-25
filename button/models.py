from django.db import models
from device.models import Device
from lamp.models import Lamp


# Create your models here.
class Button(Device):
    controlled_lamp = models.ForeignKey(Lamp, on_delete=models.CASCADE, null=True)
