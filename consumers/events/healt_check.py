from communication_protocol.communication_protocol import DeviceMessage
from .base_event import BaseEventRequest


class HealthCheckEvent(BaseEventRequest):
    """Handles health check events for devices."""

    def handle_request(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            return
        device.wifi_strength = message.payload.get("wifi_strength", -100)
        device.save(update_fields=["last_seen", "wifi_strength", "is_online"])
