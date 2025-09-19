from consumers.frontend_message.messenger import FrontendMessenger
from consumers.router_message.device_message import DeviceMessage
from consumers.events.base_event import BaseEventResponse


class SetSettings(BaseEventResponse):
    """Handles the response for setting device settings."""

    def handle_request(self, consumer, message: DeviceMessage):
        print(message)

    def handle_response(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            return
        FrontendMessenger().update_device(device)
