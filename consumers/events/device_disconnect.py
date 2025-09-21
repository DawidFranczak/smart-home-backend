from datetime import datetime

from consumers.frontend_message.messenger import FrontendMessenger
from consumers.router_message.device_message import DeviceMessage
from consumers.events.base_event import BaseEventRequest
from device.serializers.device import DeviceSerializer
from device_registry import DeviceRegistry


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
        FrontendMessenger().update_device(device.home.pk, DeviceSerializer(device).data)
