from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError
from django.contrib.auth.models import User
from channels.db import database_sync_to_async

from communication_protocol.communication_protocol import DeviceMessage


@database_sync_to_async
def validate_user(token):
    try:
        access_token = AccessToken(token)
    except TokenError:
        return None

    user_id = access_token.payload.get("user_id", 0)

    try:
        user = User.objects.get(id=user_id)
        return user
    except User.DoesNotExist:
        return None

async def send_to_router(data:DeviceMessage, router_mac:str):
    await get_channel_layer().group_send(
        f"router_{router_mac}",
        {
            "type": "router_send",
            "data": data.to_json()
        },
    )

def send_to_camera_consumer(token:str, data: str, message_event: str):
    group_name = get_camera_channel_name(token)
    async_to_sync(get_channel_layer().group_send)(
        group_name,
        {
            "type": "camera_send",
            "message_event":message_event,
            "data": data,
        }
    )
def get_camera_channel_name(token :str) -> str:
    return f"camera_{token}"