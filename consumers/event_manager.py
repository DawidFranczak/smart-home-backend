from communication_protocol.communication_protocol import DeviceMessage
from communication_protocol.message_event import MessageEvent
from communication_protocol.message_type import MessageType
from factories.event_factory import get_event_handler
from asgiref.sync import sync_to_async


class EventManager:
    def __init__(self, consumer):
        self.consumer = consumer

    @sync_to_async()
    def handle_event(self, data: DeviceMessage):
        message_event = MessageEvent(data.message_event)
        handler = get_event_handler(message_event)
        if data.message_type == MessageType.REQUEST.value:
            handler.handle_request(self.consumer, data)
        elif data.message_type == MessageType.RESPONSE.value:
            handler.handle_response(self.consumer, data)
