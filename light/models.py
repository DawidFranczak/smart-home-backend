from django.db import models

from button.models import ButtonType, MonostableButtonEvent, BistableButtonEvent
from consumers.router_message.message_event import MessageEvent
from device.models import Device


class Light(Device):
    button_type = models.CharField(
        max_length=5, choices=ButtonType.choices, default=ButtonType.BISTABLE
    )
    on = models.BooleanField(default=False)

    def available_events(self):
        if self.button_type == ButtonType.MONOSTABLE:
            return [event.value for event in MonostableButtonEvent]
        elif self.button_type == ButtonType.BISTABLE:
            return [event.value for event in BistableButtonEvent]
        else:
            return []

    def available_actions(self):
        return [
            MessageEvent.ON.value,
            MessageEvent.OFF.value,
            MessageEvent.TOGGLE.value,
        ]
