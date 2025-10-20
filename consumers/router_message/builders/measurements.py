from consumers.router_message.builders.base import build_response
from consumers.router_message.device_message import DeviceMessage


def measurements_sleeping_time_response(request: DeviceMessage, time: float):
    return build_response(request, {"sleeping_time": time})
