from asgiref.sync import async_to_sync, sync_to_async
from channels.layers import get_channel_layer

from device.models import Device
from user.frontend_message_type import FrontendMessageType


@async_to_sync
async def update_frontend_device(device: Device):
    from device.serializers.device import DeviceSerializer

    data = DeviceSerializer(device).data
    await get_channel_layer().group_send(
        f"home_{device.home.id}",
        {
            "type": "send_to_frontend",
            "action": FrontendMessageType.UPDATE_DEVICE.value,
            "data": {"status": 200, "data": data},
        },
    )


@async_to_sync
async def send_to_device(router_mac: str, data: dict):
    await get_channel_layer().group_send(
        f"router_{router_mac}",
        {"type": "router_send", "data": data},
    )
