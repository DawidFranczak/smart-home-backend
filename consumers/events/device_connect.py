from datetime import datetime

from consumers.frontend_message.frontend_message import FrontendMessage
from consumers.frontend_message.frontend_message_type import FrontendMessageType
from consumers.frontend_message.messenger import FrontendMessenger
from consumers.router_message.builders.basic import basic_response
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.messenger import DeviceMessenger
from consumers.router_message.payload.basic import DeviceConnectRequest
from consumers.events.base_event import BaseEventRequest
from device.serializers.device import DeviceSerializer
from device.serializers.router import RouterSerializer
from device_registry import DeviceRegistry
from room.serializer import RoomSerializer

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
        if device.room is not None:
            FrontendMessenger().update_frontend(
                device.home.id, DeviceSerializer(device).data
            )
            FrontendMessenger().update_frontend(
                device.home.id,
                RoomSerializer(device.room).data,
                action=FrontendMessageType.UPDATE_ROOM,
            )
        FrontendMessenger().update_frontend(
            device.home.id,
            RouterSerializer(device.home.router).data,
            action=FrontendMessageType.UPDATE_ROUTER,
        )
        response = basic_response(message, "accepted")
        DeviceMessenger().send(consumer.mac, response)

    def _create_new_device(
        self, mac: str, payload: DeviceConnectRequest, home: Home
    ) -> Device | None:
        """Creates a new device record based on the message payload."""
        fun = payload.fun
        wifi_strength = payload.wifi_strength
        register = DeviceRegistry()
        model = register.get_model(payload.fun)
        serializer = register.get_serializer(payload.fun)
        device = model.objects.create(
            home=home,
            fun=fun,
            mac=mac,
            wifi_strength=wifi_strength,
            is_online=True,
        )
        message = FrontendMessage(
            action=FrontendMessageType.NEW_DEVICE_CONNECTED,
            data=serializer(device).data,
            status=200,
        )
        FrontendMessenger().send(device.home.pk, message)
        return device
