from consumers.communication_protocol.message import Message
from consumers.communication_protocol.message_event import MessageEvent
from consumers.events.base_event import BaseEventRequest


class OnClickEvent(BaseEventRequest):

    def handle_request(self, consumer, message: Message):
        """
        Handle the incoming request for a click event.
        """
        device = self._get_device(message.device_id)
        actions_request = self.get_event_request(device, MessageEvent.ON_CLICK)
        self.send_actions_request(actions_request, consumer)

    def handle_response(self, consumer, message: Message):
        """
        Handle the response from the device for a click event.
        """
        # Process the response as needed
        pass
