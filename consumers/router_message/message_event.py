from enum import Enum


class MessageEvent(str, Enum):
    DEVICE_CONNECT = "device_connect"
    DEVICE_DISCONNECT = "device_disconnect"
    HEALTH_CHECK = "health_check"
    SET_SETTINGS = "set_settings"
    ADD_TAG = "add_tag"
    ON_READ = "on_read"
    ON_READ_SUCCESS = "on_read_success"
    ON_READ_FAILURE = "on_read_failure"
    ON_CLICK = "on_click"
    ON_HOLD = "on_hold"
    ON = "on"
    OFF = "off"
    BLINK = "blink"
    TOGGLE = "toggle"
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"
    CAMERA_OFFER = "camera_offer"
    CAMERA_ANSWER = "camera_answer"
    CAMERA_DISCONNECT = "camera_disconnect"
    CAMERA_ERROR = "camera_error"
