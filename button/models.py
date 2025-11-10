from django.db import models
from device.models import Device
from enum import Enum


class MonostableButtonEvent(Enum):
    ON_CLICK = "on_click"
    ON_HOLD = "on_hold"


class BistableButtonEvent(Enum):
    ON_TOGGLE = "on_toggle"


class ButtonType(models.TextChoices):
    MONOSTABLE = "MONO", "Monostable"
    BISTABLE = "BI", "Bistable"


class Button(Device):
    button_type = models.CharField(
        max_length=5, choices=ButtonType.choices, default=ButtonType.MONOSTABLE
    )

    def available_events(self):
        if self.button_type == ButtonType.MONOSTABLE:
            return [event.value for event in MonostableButtonEvent]
        elif self.button_type == ButtonType.BISTABLE:
            return [event.value for event in BistableButtonEvent]
        else:
            return []
