from uuid import uuid4

from aquarium.models import Aquarium
from communication_protocol.communication_protocol import DeviceMessage
from communication_protocol.message_event import MessageEvent
from communication_protocol.message_type import MessageType


def set_fluo_request(instance:Aquarium, value:bool):
    return _message_request(MessageEvent.SET_FLUO, instance.mac, {"value": value})

def set_led_request(instance:Aquarium, value:bool):
    return _message_request(MessageEvent.SET_LED, instance.mac, {"value": value})

def set_rgb_request(instance:Aquarium, rgb:dict):
    return _message_request(MessageEvent.SET_RGB, instance.mac, rgb)

def _message_request(message_event:MessageEvent, device_id:str,payload:dict):
    return DeviceMessage(
        message_id=uuid4().hex,
        message_type=MessageType.REQUEST,
        message_event=message_event,
        device_id=device_id,
        payload=payload,
    )
