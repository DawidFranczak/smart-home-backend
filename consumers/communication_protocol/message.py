import re
from pydantic import BaseModel, field_validator, model_validator, ValidationError
from .message_event import MessageEvent
from .message_type import MessageType
from consumers.communication_protocol.payload.mapper import PAYLOAD_MAPPING


class Message(BaseModel):
    message_type: MessageType
    message_event: MessageEvent
    device_id: str
    message_id: str
    payload: dict | BaseModel

    @field_validator("device_id", mode="after")
    def validate_mac(cls, value):
        pattern = r"^([0-9a-fA-F]{2}[:-]){5}([0-9a-fA-F]){2}$"
        if not re.match(pattern, value):
            raise ValidationError("Invalid MAC address")
        return value

    @model_validator(mode="after")
    def validate_payload(self):
        payload_type = PAYLOAD_MAPPING.get(self.message_event, None)
        if payload_type is None:
            raise ValidationError(
                f"Unsupported payload type. Did you forget to register {self.message_event.value}?"
            )
        model = (
            payload_type[0]
            if self.message_type == MessageType.REQUEST
            else payload_type[1]
        )
        self.payload = model(**self.payload)
        return self
