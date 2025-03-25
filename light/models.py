from django.db import models
from device.models import Device


# Create your models here.
class Light(Device):
    on = models.BooleanField(default=False)
