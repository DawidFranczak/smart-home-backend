from uuid import uuid4

from communication_protocol.communication_protocol import DeviceMessage
from communication_protocol.message_event import MessageEvent
from communication_protocol.message_type import MessageType


def set_settings_request(instance, payload: dict):
    return message_request(MessageEvent.SET_SETTINGS, instance.mac, payload)


def message_request(message_event: MessageEvent, device_id: str, payload: dict):
    return DeviceMessage(
        message_id=uuid4().hex,
        message_type=MessageType.REQUEST,
        message_event=message_event,
        device_id=device_id,
        payload=payload,
    )


def set_settings_response(message_id, device_data, serialized_device_data):
    return DeviceMessage(
        message_id=message_id,
        message_event=MessageEvent.SET_SETTINGS,
        message_type=MessageType.RESPONSE,
        device_id=device_data,
        payload=serialized_device_data,
    )


def message_response(
    message_id: str, message_event: MessageEvent, device_id: str, payload: dict
) -> DeviceMessage:
    return DeviceMessage(
        message_id=message_id,
        message_type=MessageType.RESPONSE,
        message_event=message_event,
        device_id=device_id,
        payload=payload,
    )
