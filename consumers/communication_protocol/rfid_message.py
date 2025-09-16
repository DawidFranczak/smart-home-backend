from consumers.communication_protocol.message import Message
from consumers.communication_protocol.device_message import (
    message_request,
    message_response,
)
from consumers.communication_protocol.message_event import MessageEvent
from rfid.models import Rfid


def add_card_request(instance: Rfid, name: str) -> Message:
    return message_request(MessageEvent.ADD_TAG, instance.mac, {"name": name})


def on_read_success_request() -> Message:
    return message_response(MessageEvent.ON_READ_SUCCESS, "success", {})
