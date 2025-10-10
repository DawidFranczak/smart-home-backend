from enum import Enum


class MessageEvent(str, Enum):
    # Basic events
    GET_CONNECTED_DEVICES = "get_connected_devices"
    DEVICE_CONNECT = "device_connect"
    DEVICE_DISCONNECT = "device_disconnect"
    HEALTH_CHECK = "health_check"
    SET_SETTINGS = "set_settings"
    GET_SETTINGS = "get_settings"

    # Button events
    ON_CLICK = "on_click"
    ON_HOLD = "on_hold"

    # Light events
    ON = "on"
    OFF = "off"
    BLINK = "blink"
    TOGGLE = "toggle"

    # RFID events
    ADD_TAG = "add_tag"
    ON_READ = "on_read"
    ON_READ_SUCCESS = "on_read_success"
    ON_READ_FAILURE = "on_read_failure"
    ACCESS_GRANTED = "access_granted"
    ACCESS_DENIED = "access_denied"

    # Camera events
    CAMERA_OFFER = "camera_offer"
    CAMERA_ANSWER = "camera_answer"
    CAMERA_DISCONNECT = "camera_disconnect"
    CAMERA_ERROR = "camera_error"

    # Sensor events
    MEASURE_TEMPERATURE = "measure_temperature"
    MEASURE_HUMIDITY = "measure_humidity"
