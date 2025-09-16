from consumers.communication_protocol.message import Message
from consumers.events.base_event import BaseEventResponse


class OnEvent(BaseEventResponse):

    def handle_response(self, consumer, message: Message):
        pass
