from typing import Literal

from pydantic import BaseModel, field_validator
from device_registry import DeviceRegistry


class EmptyRequest(BaseModel):
    pass


class EmptyResponse(BaseModel):
    pass


class BasicResponse(BaseModel):
    message: Literal["accepted", "rejected"]


class DeviceConnectRequest(BaseModel):
    wifi_strength: int
    fun: str

    @field_validator("fun")
    def validate_fun(cls, value):
        if value not in DeviceRegistry().devices:
            raise ValueError(f"Invalid device fun: {value}")
        return value


class DeviceDisconnectRequest(BaseModel):
    pass


class HealthCheckRequest(BaseModel):
    wifi_strength: int


class SetSettingsRequest(BaseModel):
    pass


class DeviceDisconnectResponse(BaseModel):
    pass


class HealthCheckResponse(BaseModel):
    pass


class SetSettingsResponse(BaseModel):
    pass
