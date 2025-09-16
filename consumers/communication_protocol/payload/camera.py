from pydantic import BaseModel


class CameraOfferPayload(BaseModel):
    pass


class CameraAnswerPayload(BaseModel):
    pass


class CameraDisconnectPayload(BaseModel):
    pass


class CameraErrorPayload(BaseModel):
    pass
