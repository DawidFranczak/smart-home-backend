from consumers.communication_protocol.message import Message
from consumers.events.base_event import BaseEventResponse
from utils.web_socket_message import update_frontend_device


class SetSettings(BaseEventResponse):
    """Handles the response for setting device settings."""

    def handle_response(self, consumer, message: Message):
        device = self._get_device(message.device_id)
        if not device:
            return
        update_frontend_device(device, 200)
