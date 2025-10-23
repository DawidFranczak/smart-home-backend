from pydantic import BaseModel
from datetime import datetime


class TemperatureRequest(BaseModel):
    temperature: float


class HumidityRequest(BaseModel):
    humidity: float


class TempHumRequest(TemperatureRequest, HumidityRequest):
    pass
