from consumers.router_message.device_message import DeviceMessage
from .base_event import BaseEventRequest


class HealthCheckEvent(BaseEventRequest):
    """Handles health check events for devices."""

    def handle_request(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            return
        device.wifi_strength = message.payload.wifi_strength
        device.save(update_fields=["last_seen", "wifi_strength", "is_online"])
