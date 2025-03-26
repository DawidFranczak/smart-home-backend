from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

from .models import Rfid
from communication_protocol.rfid_message import add_card_request


def add_card(instance: Rfid, name: str) -> None:
    message = add_card_request(instance, name)
    async_to_sync(get_channel_layer().group_send)(
        f"router_{instance.get_router_mac()}",
        {"type": "router_send", "data": message.to_json()},
    )
