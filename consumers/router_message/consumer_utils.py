from asgiref.sync import sync_to_async

from consumers.router_message.builders.base import build_request
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.message_event import MessageEvent


@sync_to_async
def lamp_turn_on_request(mac: str) -> DeviceMessage:
    return build_request(MessageEvent.ON, mac, {"reverse": False})
