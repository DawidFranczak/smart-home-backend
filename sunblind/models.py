from django.db import models
from device.models import Device


# Create your models here.
class Sunblind(Device):
    value = models.IntegerField(default=0)
