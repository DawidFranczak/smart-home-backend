from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Rfid
from consumers.router_message.builders.rfid import add_tag_request


def add_card(instance: Rfid, name: str) -> None:
    message = add_tag_request(instance, name)
    async_to_sync(get_channel_layer().group_send)(
        f"router_{instance.get_router_mac()}",
        {"type": "router_send", "data": message.to_json()},
    )
