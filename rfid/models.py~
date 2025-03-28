from django.utils import timezone
from django.db import models
from device.models import Device
from lamp.models import Lamp


# Create your models here.
class Rfid(Device):
    controlled_lamp = models.ForeignKey(Lamp, on_delete=models.CASCADE, null=True)


class Card(models.Model):
    rfid = models.ForeignKey(Rfid, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=50, default="")
    uid = models.IntegerField(unique=True)
    last_used = models.DateTimeField(default=timezone.now)
