from annotated_types.test_cases import cases

from consumers.events.base_event import BaseEventRequest
from consumers.frontend_message.messenger import FrontendMessenger
from consumers.rabbitmq_publisher import get_publisher, QueueNames
from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.message_event import MessageEvent
from device.models import Device
from device.serializers.device import DeviceSerializer
from device_registry import DeviceRegistry
from light.models import Light


def light_state_change(pk: int, message: DeviceMessage):
    device = Light.objects.get(pk=pk)
    device.on = message.payload.state == MessageEvent.ON
    device.save(update_fields=["on"])
    FrontendMessenger().update_frontend(device.home.pk, DeviceSerializer(device).data)
    publisher = get_publisher()
    publisher.send_message(QueueNames.SENSORS, message)


state_mapper = {"light": light_state_change}


class StateChange(BaseEventRequest):

    def handle_request(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        if not device:
            return
        f = state_mapper[device.fun]
        if not f:
            raise Exception(f"State mapper for {device.fun} not registered")
        f(device.pk, message)
