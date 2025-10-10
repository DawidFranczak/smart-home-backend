from consumers.router_message.device_message import DeviceMessage
from consumers.events.base_event import BaseEventResponse


class BlinkEvent(BaseEventResponse):

    def handle_response(self, consumer, message: DeviceMessage):
        pass
