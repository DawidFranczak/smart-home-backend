from communication_protocol.communication_protocol import DeviceMessage
from consumers.events.base_event import BaseEventRequest, BaseEventResponse
from utils.web_socket_message import update_frontend_device


class SetSettings(BaseEventResponse):
    """Handles the response for setting device settings."""

    def handle_response(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            return
        update_frontend_device(device, 200)
