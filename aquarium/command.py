from datetime import time
from uuid import uuid4

from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.db.models.expressions import result

from aquarium.models import Aquarium
from communication_protocol.aquarium_message import set_fluo_request, set_led_request, set_rgb_request
from communication_protocol.communication_protocol import DeviceMessage
from communication_protocol.message_event import MessageEvent
from communication_protocol.message_type import MessageType
from utils.check_hour_in_range import check_hour_in_range


def change_rgb_request(instance: Aquarium, rgb: dict):
    message = set_rgb_request(instance, rgb)
    async_to_sync(get_channel_layer().group_send)(
        f"router_{instance.get_router_mac()}",
        {"type": "router_send", "data": message.to_json()},
    )


def change_fluo_lamp_state_request(instance: Aquarium, state: bool):
    message = set_fluo_request(instance, state)
    async_to_sync(get_channel_layer().group_send)(
        f"router_{instance.get_router_mac()}",
        {"type": "router_send", "data": message.to_json()},
    )


def change_led_state_request(instance: Aquarium, state: bool):
    message = set_led_request(instance, state)
    async_to_sync(get_channel_layer().group_send)(
        f"router_{instance.get_router_mac()}",
        {"type": "router_send", "data": message.to_json()},
    )


def check_and_change_led_time_request(instance: Aquarium, led_start: time, led_stop: time):
    led_result = check_hour_in_range(led_start, led_stop)
    if led_result == instance.led_mode:
        return led_result
    message = set_led_request(instance, led_result)
    async_to_sync(get_channel_layer().group_send)(
        f"router_{instance.get_router_mac()}",
        {"type": "router_send", "data": message.to_json()},
    )
    return led_result


def check_and_change_fluo_lamp_time_request(
    instance: Aquarium, fluo_start: time, fluo_stop: time
):
    fluo_result = check_hour_in_range(fluo_start, fluo_stop)
    if fluo_result == instance.fluo_mode:
        return fluo_result
    message = set_fluo_request(instance, fluo_result)
    async_to_sync(get_channel_layer().group_send)(
        f"router_{instance.get_router_mac()}",
        {"type": "router_send", "data": message.to_json()},
    )

    return fluo_result


def change_mode(instance: Aquarium, mode: bool):
    if not mode:
        return
    check_and_change_fluo_lamp_time_request(instance, instance.fluo_start, instance.fluo_stop)
    check_and_change_led_time_request(instance, instance.led_start, instance.led_stop)
