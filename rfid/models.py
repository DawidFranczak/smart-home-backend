from enum import Enum
from django.utils import timezone
from django.db import models
from device.models import Device
from lamp.models import Lamp


class RfidEvent(Enum):
    ON_READ = "on_read"
    ON_READ_SUCCESS = "on_read_success"
    ON_READ_FAILURE = "on_read_failure"
    ON_CLICK = "on_click"
    ON_HOLD = "on_hold"


# Create your models here.
class Rfid(Device):

    @staticmethod
    def available_events():
        return [event.value for event in RfidEvent]


class Card(models.Model):
    rfid = models.ForeignKey(Rfid, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=50, default="")
    uid = models.BigIntegerField(unique=True)
    last_used = models.DateTimeField(default=timezone.now)
