from asgiref.sync import sync_to_async

from communication_protocol.communication_protocol import DeviceMessage
from communication_protocol.device_message import message_request
from communication_protocol.message_event import MessageEvent
from .models import Lamp


@sync_to_async
def lamp_turn_on_request(device: Lamp) -> DeviceMessage:
    return message_request(MessageEvent.TURN_ON, device.mac, {"reverse": False})
