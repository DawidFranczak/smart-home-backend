from consumers.events.base_event import BaseEventRequest, BaseEventResponse


class GetConnectedDevices(BaseEventRequest, BaseEventResponse):

    def handle_request(self, consumer, message):
        print(f"GetConnectedDevices REQUEST", message)

    def handle_response(self, consumer, message):
        print(f"GetConnectedDevices RESPONSE", message)
