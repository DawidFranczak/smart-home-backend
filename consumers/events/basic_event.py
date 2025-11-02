from consumers.events.base_event import BaseEventRequest, BaseEventResponse
from consumers.router_message.device_message import DeviceMessage


class Basic(BaseEventRequest, BaseEventResponse):

    def handle_request(self, consumer, message: DeviceMessage):
        device = self._get_device(message.device_id)
        actions_request = self.get_event_request(device, message.message_event)
        self.send_actions_request(actions_request, consumer)

    def handle_response(self, consumer, message: DeviceMessage):
        pass
