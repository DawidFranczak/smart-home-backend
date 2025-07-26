from communication_protocol.communication_protocol import DeviceMessage
from consumers.events.base_event import BaseEventResponse


class AccessDeniedEvent(BaseEventResponse):

    def handle_response(self, consumer, message: DeviceMessage):
        pass
