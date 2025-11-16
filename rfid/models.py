from enum import Enum
from django.utils import timezone
from django.db import models

from button.models import ButtonType, MonostableButtonEvent
from device.models import Device


class RfidEvent(Enum):
    ON_READ = "on_read"
    ON_READ_SUCCESS = "on_read_success"
    ON_READ_FAILURE = "on_read_failure"


class RfidAction(Enum):
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"


class Rfid(Device):
    button_type = models.CharField(
        max_length=5, choices=ButtonType.choices, default=ButtonType.MONOSTABLE
    )

    def available_events(self):
        return [event.value for event in RfidEvent] + [
            event.value for event in MonostableButtonEvent
        ]

    def available_actions(self):
        return [action.value for action in RfidAction]


class Card(models.Model):
    rfid = models.ForeignKey(Rfid, on_delete=models.CASCADE, related_name="cards")
    name = models.CharField(max_length=50, default="")
    uid = models.BigIntegerField(unique=True)
    last_used = models.DateTimeField(default=timezone.now)
