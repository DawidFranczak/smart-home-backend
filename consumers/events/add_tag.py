from consumers.communication_protocol.message import Message
from consumers.communication_protocol.message_event import MessageEvent
from consumers.events.base_event import BaseEventResponse
from rfid.models import Rfid, Card
from utils.web_socket_message import update_frontend_device


class AddTagEvent(BaseEventResponse):

    def handle_response(self, consumer, message: Message):
        uid = message.payload.get("uid", None)
        name = message.payload.get("name", None)
        if not uid:
            return

        device = self._get_device(message.device_id)
        if not device:
            return

        rfid = Rfid.objects.get(pk=device.id)
        status = 400
        if uid:
            cards = Card.objects.filter(uid=uid)
            if cards.exists():
                status = 409
            else:
                Card.objects.create(
                    rfid=rfid,
                    uid=uid,
                    name=name,
                )
                status = 201
        rfid.pending.remove(MessageEvent.ADD_TAG.value)
        rfid.save(update_fields=["pending"])
        update_frontend_device(rfid, status)
