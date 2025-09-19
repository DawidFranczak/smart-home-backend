from consumers.events.base_event import BaseEventRequest
from consumers.frontend_message.messenger import FrontendMessenger
from consumers.router_message.builders.basic import data_response
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.messenger import DeviceMessenger
from device_registry import DeviceRegistry


class GetSettings(BaseEventRequest):
    """Handles the response for setting device settings."""

    def handle_request(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            return
        device_registry = DeviceRegistry()

        model = device_registry.get_model(device.fun)
        device = model.objects.get(id=device.pk)

        serializer = device_registry.get_serializer(device.fun)
        FrontendMessenger().update_device(device.home.id, serializer(device).data)

        serializer_device = device_registry.get_serializer_device(device.fun)
        response = data_response(message, serializer_device(device).data)
        DeviceMessenger().send(consumer.mac, response)
