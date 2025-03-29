from communication_protocol.communication_protocol import DeviceMessage
from communication_protocol.device_message import message_request, message_response
from communication_protocol.message_event import MessageEvent
from rfid.check_uid_response import CheckUIDResponse
from rfid.models import Rfid


def add_card_request(instance: Rfid, name: str) -> DeviceMessage:
    return message_request(MessageEvent.ADD_TAG, instance.mac, {"name": name})


def check_uid_response(
    mac: str, message_id: str, message: CheckUIDResponse
) -> DeviceMessage:
    return message_response(
        message_id, MessageEvent.CHECK_UID, mac, {"message": message.value}
    )
