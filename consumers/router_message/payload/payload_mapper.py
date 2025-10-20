from typing import Tuple, Type

from consumers.router_message.payload.basic import *
from consumers.router_message.payload.camera import *
from consumers.router_message.payload.measurement import (
    TemperatureRequest,
    HumidityRequest,
    TempHumRequest,
)
from consumers.router_message.payload.rfid import *
from consumers.router_message.payload.lamp import *
from consumers.router_message.payload.button import *

from consumers.router_message.message_event import MessageEvent

PAYLOAD_MAPPING: dict[MessageEvent, Tuple[Type[BaseModel], Type[BaseModel]]] = {
    MessageEvent.GET_CONNECTED_DEVICES: (EmptyRequest, BasicResponse),
    MessageEvent.DEVICE_CONNECT: (DeviceConnectRequest, BasicResponse),
    MessageEvent.DEVICE_DISCONNECT: (DeviceDisconnectRequest, BasicResponse),
    MessageEvent.HEALTH_CHECK: (HealthCheckRequest, BasicResponse),
    MessageEvent.SET_SETTINGS: (SerializerDataResponse, BasicResponse),
    MessageEvent.GET_SETTINGS: (EmptyRequest, SerializerDataResponse),
    MessageEvent.ADD_TAG: (SerializerDataResponse, AddTagResponse),
    MessageEvent.ON_READ: (OnReadRequest, BasicResponse),
    MessageEvent.ON_READ_SUCCESS: (SerializerDataResponse, BasicResponse),
    MessageEvent.ON_READ_FAILURE: (SerializerDataResponse, BasicResponse),
    MessageEvent.ON_CLICK: (SerializerDataResponse, BasicResponse),
    MessageEvent.ON_HOLD: (SerializerDataResponse, BasicResponse),
    MessageEvent.ON: (SerializerDataResponse, BasicResponse),
    MessageEvent.OFF: (SerializerDataResponse, BasicResponse),
    MessageEvent.BLINK: (SerializerDataResponse, BasicResponse),
    MessageEvent.TOGGLE: (SerializerDataResponse, BasicResponse),
    MessageEvent.ACCESS_GRANTED: (AccessGrantedPayload, BasicResponse),
    MessageEvent.ACCESS_DENIED: (AccessDeniedPayload, BasicResponse),
    MessageEvent.CAMERA_OFFER: (CameraOfferRequest, BasicResponse),
    MessageEvent.CAMERA_ANSWER: (EmptyRequest, CameraAnswerResponse),
    MessageEvent.CAMERA_DISCONNECT: (CameraDisconnectPayload, BasicResponse),
    MessageEvent.CAMERA_ERROR: (CameraError, CameraError),
    MessageEvent.ON_MEASURE_TEMPERATURE: (TemperatureRequest, SerializerDataResponse),
    MessageEvent.ON_MEASURE_HUMIDITY: (HumidityRequest, SerializerDataResponse),
    MessageEvent.ON_MEASUREMENT_TEMP_HUM: (TempHumRequest, SerializerDataResponse),
}
