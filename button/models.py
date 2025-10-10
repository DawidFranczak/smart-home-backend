from device.models import Device
from enum import Enum


class ButtonEvent(Enum):
    ON_CLICK = "on_click"
    ON_HOLD = "on_hold"


class Button(Device):

    @staticmethod
    def available_events():
        return [event.value for event in ButtonEvent]
