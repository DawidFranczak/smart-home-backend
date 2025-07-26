from asgiref.sync import async_to_sync
from datetime import datetime

from communication_protocol.communication_protocol import DeviceMessage
from communication_protocol.device_message import set_settings_response
from consumers.events.base_event import BaseEventRequest
from device_registry import DeviceRegistry
from utils.web_socket_message import update_frontend_device

from user.models import Home
from device.models import Device


class DeviceConnectEvent(BaseEventRequest):
    """Handles device connection events by updating or creating device records."""

    def handle_request(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            device = self._create_new_device(message, consumer.home)
            if not device:
                return
        device.last_seen = datetime.now()
        device.is_online = True
        device.pending = []
        device.save(update_fields=["last_seen", "is_online", "pending"])
        register = DeviceRegistry()
        serializer = register.get_serializer_device(device.fun)
        message = set_settings_response(
            message.message_id, message.device_id, serializer(device).data
        )
        async_to_sync(consumer.router_send)(message.to_json())
        update_frontend_device(device)

    def _create_new_device(self, message: DeviceMessage, home: Home) -> Device | None:
        """Creates a new device record based on the message payload."""
        try:
            fun = message.payload["fun"]
            ip = message.payload["ip"]
            port = message.payload["port"]
            wifi_strength = message.payload["wifi_strength"]
        except KeyError:
            return None
        register = DeviceRegistry()
        model = register.get_model(message.payload["fun"])
        return model.objects.create(
            home=home,
            ip=ip,
            port=port,
            fun=fun,
            mac=message.device_id,
            wifi_strength=wifi_strength,
            is_online=True,
        )
