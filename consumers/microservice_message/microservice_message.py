from pydantic import BaseModel

from consumers.router_message.message_event import MessageEvent


class MicroserviceMessage(BaseModel):
    message_event: MessageEvent
    device_id: int
    home_id: int
    payload: dict
