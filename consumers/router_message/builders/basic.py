import time
from typing import Literal

from consumers.router_message.builders.base import build_response, build_request
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.message_event import MessageEvent
from device.models import Event


def basic_response(
    message: DeviceMessage, status_type: Literal["accepted", "rejected"]
) -> DeviceMessage:
    return build_response(message, {"status": status_type})


def set_settings_response(
    message: DeviceMessage, serializer_data: dict
) -> DeviceMessage:
    return build_response(message, serializer_data)


def set_settings_request(mac: str, payload: dict) -> DeviceMessage:
    return build_request(MessageEvent.SET_SETTINGS, mac, payload)


def health_check_response(message: DeviceMessage) -> DeviceMessage:
    return build_response(message, {"timestamp": time.time()})


def get_event_request(event: Event):
    return build_request(
        MessageEvent(event.action), event.target_device.mac, event.extra_settings
    )
