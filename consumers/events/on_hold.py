from consumers.communication_protocol.message import Message
from consumers.communication_protocol.message_event import MessageEvent
from consumers.events.base_event import BaseEventRequest


class OnHoldEvent(BaseEventRequest):

    def handle_request(self, consumer, message: Message):
        """
        Handle the incoming request for a hold event.
        """
        device = self._get_device(message.device_id)
        actions_request = self.get_event_request(device, MessageEvent.ON_HOLD)
        self.send_actions_request(actions_request, consumer)
