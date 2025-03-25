from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

from device.models import Router


def send_data(instance, data):
    channel_layer = get_channel_layer()
    router = get_router(instance)
    async_to_sync(channel_layer.group_send)(
        f"router_{router.mac}", {"type": "router_send", "ip": instance.ip, "data": data}
    )


def get_router(instance):
    return Router.objects.get(home=instance.room.home)
