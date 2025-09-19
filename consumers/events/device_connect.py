from datetime import datetime

from consumers.frontend_message.messenger import FrontendMessenger
from consumers.router_message.builders.basic import set_settings_response
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.messenger import DeviceMessenger
from consumers.router_message.payload.basic import DeviceConnectRequest
from consumers.events.base_event import BaseEventRequest
from device_registry import DeviceRegistry

from user.models import Home
from device.models import Device


class DeviceConnectEvent(BaseEventRequest):
    """Handles device connection events by updating or creating device records."""

    def handle_request(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            device = self._create_new_device(
                message.device_id, message.payload, consumer.home
            )
            if not device:
                return
        device.last_seen = datetime.now()
        device.is_online = True
        device.pending = []
        device.save(update_fields=["last_seen", "is_online", "pending"])
        register = DeviceRegistry()
        serializer = register.get_serializer_device(device.fun)
        model = register.get_model(device.fun)
        message = set_settings_response(
            message,
            serializer(model.objects.get(pk=device.pk)).data,
        )
        DeviceMessenger().send(consumer.mac, message)
        FrontendMessenger().update_device(device)

    def _create_new_device(
        self, mac: str, payload: DeviceConnectRequest, home: Home
    ) -> Device | None:
        """Creates a new device record based on the message payload."""
        fun = payload.fun
        wifi_strength = payload.wifi_strength
        register = DeviceRegistry()
        model = register.get_model(payload.fun)
        return model.objects.create(
            home=home,
            fun=fun,
            mac=mac,
            wifi_strength=wifi_strength,
            is_online=True,
        )
