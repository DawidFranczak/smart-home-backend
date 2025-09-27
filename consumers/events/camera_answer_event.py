from consumers.router_message.device_message import DeviceMessage
from consumers.events.base_event import BaseEventResponse

from consumers.utils import send_to_camera_consumer


class CameraAnswerEvent(BaseEventResponse):

    def handle_response(self, consumer, message: DeviceMessage):
        payload = message.payload
        token = payload.token
        data = payload.answer.model_dump_json()
        send_to_camera_consumer(token, data, message.message_event)
