from consumers.communication_protocol.message import Message
from consumers.communication_protocol.message_event import MessageEvent
from consumers.events.base_event import BaseEventRequest
from rfid.models import Card


class OnReadEvent(BaseEventRequest):
    """Handles the RFID card read event."""

    def handle_request(self, consumer, message: Message):
        """Check if the RFID card is registered and send the appropriate event."""
        uid: str | None = message.payload.get("uid", None)
        if not uid:
            return
        device = self._get_device(message.device_id)
        result = Card.objects.filter(rfid=device, uid=uid).exists()
        event = MessageEvent.ON_READ_SUCCESS if result else MessageEvent.ON_READ_FAILURE
        actions_request = self.get_event_request(device, event)
        self.send_actions_request(actions_request, consumer)
