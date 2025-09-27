from consumers.events.get_settings import GetSettings
from consumers.router_message.message_event import MessageEvent
from consumers.events.access_denied import AccessDeniedEvent
from consumers.events.access_granted import AccessGrantedEvent
from consumers.events.add_tag import AddTagEvent
from consumers.events.blink import BlinkEvent
from consumers.events.camera_answer_event import CameraAnswerEvent
from consumers.events.device_connect import DeviceConnectEvent
from consumers.events.device_disconnect import DeviceDisconnectEvent
from consumers.events.healt_check import HealthCheckEvent
from consumers.events.on_click import OnClickEvent
from consumers.events.on_hold import OnHoldEvent
from consumers.events.on_read import OnReadEvent
from consumers.events.camera_error_event import CameraErrorEvent
from consumers.events.set_settings import SetSettings
from consumers.events.on import OnEvent
from consumers.events.toggle import ToggleEvent


def get_event_handler(event_type: MessageEvent):
    """
    Factory function to get the appropriate event handler based on the event type.

    Args:
        event_type (MessageEvent): The type of the event (e.g., 'DEVICE_CONNECT', 'ON_CLICK').

    Returns:
        Callable: The event handler function for the specified event type.
    """
    handlers = {
        MessageEvent.DEVICE_CONNECT: DeviceConnectEvent(),
        MessageEvent.DEVICE_DISCONNECT: DeviceDisconnectEvent(),
        MessageEvent.HEALTH_CHECK: HealthCheckEvent(),
        MessageEvent.SET_SETTINGS: SetSettings(),
        MessageEvent.GET_SETTINGS: GetSettings(),
        MessageEvent.ON_CLICK: OnClickEvent(),
        MessageEvent.ON_HOLD: OnHoldEvent(),
        MessageEvent.ON_READ: OnReadEvent(),
        MessageEvent.ON: OnEvent(),
        MessageEvent.BLINK: BlinkEvent(),
        MessageEvent.TOGGLE: ToggleEvent(),
        MessageEvent.ACCESS_GRANTED: AccessGrantedEvent(),
        MessageEvent.ACCESS_DENIED: AccessDeniedEvent(),
        MessageEvent.ADD_TAG: AddTagEvent(),
        MessageEvent.CAMERA_ANSWER: CameraAnswerEvent(),
        MessageEvent.CAMERA_ERROR: CameraErrorEvent(),
    }
    handler = handlers.get(event_type, None)
    if handler is None:
        raise ValueError(
            f"No handler found for event type: {event_type} did you forget to add it to the factory?"
        )
    return handler
