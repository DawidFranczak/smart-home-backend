from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from device.models import Device
from consumers.frontend_message_type import FrontendMessageType


def update_frontend_device(device: Device, status=200):
    from device.serializers.device import DeviceSerializer

    data = DeviceSerializer(device).data
    async_to_sync(get_channel_layer().group_send)(
        f"home_{device.home.id}",
        {
            "type": "send_to_frontend",
            "action": FrontendMessageType.UPDATE_DEVICE.value,
            "data": {"status": status, "data": data},
        },
    )


@async_to_sync
async def send_to_device(router_mac: str, data: dict):
    await get_channel_layer().group_send(
        f"router_{router_mac}",
        {"type": "router_send", "data": data},
    )
