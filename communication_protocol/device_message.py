from communication_protocol.communication_protocol import DeviceMessage
from communication_protocol.message_event import MessageEvent
from communication_protocol.message_type import MessageType


def set_settings_response(message_id, device_data, serialized_device_data):
    return DeviceMessage(
        message_id=message_id,
        message_event=MessageEvent.SET_SETTINGS,
        message_type=MessageType.RESPONSE,
        device_id=device_data,
        payload=serialized_device_data,
    )
