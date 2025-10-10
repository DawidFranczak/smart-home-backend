from enum import Enum
from django.utils import timezone
from django.db import models
from device.models import Device


class RfidEvent(Enum):
    ON_READ = "on_read"
    ON_READ_SUCCESS = "on_read_success"
    ON_READ_FAILURE = "on_read_failure"
    ON_CLICK = "on_click"
    ON_HOLD = "on_hold"


class RfidAction(Enum):
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"


class Rfid(Device):

    @staticmethod
    def available_events():
        return [event.value for event in RfidEvent]

    @staticmethod
    def available_actions():
        return [action.value for action in RfidAction]


class Card(models.Model):
    rfid = models.ForeignKey(Rfid, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=50, default="")
    uid = models.BigIntegerField(unique=True)
    last_used = models.DateTimeField(default=timezone.now)
