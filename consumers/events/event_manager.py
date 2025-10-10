from consumers.router_message.device_message import DeviceMessage
from consumers.router_message.message_type import MessageType
from consumers.events.event_factory import get_event_handler
from asgiref.sync import sync_to_async


class EventManager:
    def __init__(self, consumer):
        self.consumer = consumer

    @sync_to_async()
    def handle_event(self, data: DeviceMessage):
        handler = get_event_handler(data.message_event)
        if data.message_type == MessageType.REQUEST.value:
            handler.handle_request(self.consumer, data)
        elif data.message_type == MessageType.RESPONSE.value:
            handler.handle_response(self.consumer, data)
