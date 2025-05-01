from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from user.frontend_message_type import FrontendMessageType


@async_to_sync
async def update_frontend_device(home_id: int, data: dict):
    await get_channel_layer().group_send(
        f"home_{home_id}",
        {
            "type": "send_to_frontend",
            "action": FrontendMessageType.UPDATE_DEVICE.value,
            "data": {"status": 200, "data": data},
        },
    )
