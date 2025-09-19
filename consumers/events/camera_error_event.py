from consumers.router_message.device_message import DeviceMessage
from consumers.events.base_event import BaseEventResponse
from consumers.utils import send_to_camera_consumer


class CameraErrorEvent(BaseEventResponse):

    def handle_response(self, consumer, message: DeviceMessage):
        payload = message.payload
        token = payload.get("token")
        data = payload.get("error")
        if not token or not data:
            return

        send_to_camera_consumer(token, data, message.message_event)
