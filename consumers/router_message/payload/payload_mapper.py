from typing import Tuple, Type

from consumers.router_message.payload.basic import *
from consumers.router_message.payload.camera import *
from consumers.router_message.payload.rfid import *
from consumers.router_message.payload.lamp import *
from consumers.router_message.payload.button import *

from consumers.router_message.message_event import MessageEvent

PAYLOAD_MAPPING: dict[MessageEvent, Tuple[Type[BaseModel], Type[BaseModel]]] = {
    MessageEvent.DEVICE_CONNECT: (DeviceConnectRequest, BasicResponse),
    MessageEvent.DEVICE_DISCONNECT: (DeviceDisconnectRequest, BasicResponse),
    MessageEvent.HEALTH_CHECK: (HealthCheckRequest, BasicResponse),
    MessageEvent.SET_SETTINGS: (SetSettingsRequest, SerializerDataResponse),
    MessageEvent.ADD_TAG: (AddTagPayload, BasicResponse),
    MessageEvent.ON_READ: (OnReadPayload, BasicResponse),
    MessageEvent.ON_READ_SUCCESS: (OnReadSuccessPayload, BasicResponse),
    MessageEvent.ON_READ_FAILURE: (OnReadFailurePayload, BasicResponse),
    MessageEvent.ON_CLICK: (OnClickPayload, BasicResponse),
    MessageEvent.ON_HOLD: (OnHoldPayload, BasicResponse),
    MessageEvent.ON: (OnPayload, BasicResponse),
    MessageEvent.OFF: (OffPayload, BasicResponse),
    MessageEvent.BLINK: (BlinkPayload, BasicResponse),
    MessageEvent.TOGGLE: (TogglePayload, BasicResponse),
    MessageEvent.ACCESS_GRANTED: (AccessGrantedPayload, BasicResponse),
    MessageEvent.ACCESS_DENIED: (AccessDeniedPayload, BasicResponse),
    MessageEvent.CAMERA_OFFER: (CameraOfferPayload, BasicResponse),
    MessageEvent.CAMERA_ANSWER: (CameraAnswerPayload, BasicResponse),
    MessageEvent.CAMERA_DISCONNECT: (CameraDisconnectPayload, BasicResponse),
    MessageEvent.CAMERA_ERROR: (CameraErrorPayload, BasicResponse),
}
