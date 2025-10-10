from pydantic import BaseModel
from datetime import datetime


class TemperatureRequest(BaseModel):
    temperature: float
    timestamp: datetime


class HumidityRequest(BaseModel):
    humidity: float
    timestamp: datetime
