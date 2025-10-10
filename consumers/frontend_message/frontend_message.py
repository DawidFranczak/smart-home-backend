from pydantic import BaseModel

from consumers.frontend_message.frontend_message_type import FrontendMessageType


class FrontendMessage(BaseModel):
    action: FrontendMessageType
    status: int
    data: dict
