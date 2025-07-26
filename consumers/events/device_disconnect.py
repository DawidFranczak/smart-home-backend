from datetime import datetime

from communication_protocol.communication_protocol import DeviceMessage
from consumers.events.base_event import BaseEventRequest
from utils.web_socket_message import update_frontend_device


class DeviceDisconnectEvent(BaseEventRequest):
    """
    Event triggered when a device disconnects.
    """

    def handle_request(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            return
        device.last_seen = datetime.now()
        device.is_online = False
        device.pending = []
        device.save(update_fields=["last_seen", "is_online", "pending"])
        update_frontend_device(device)
