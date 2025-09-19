from asgiref.sync import async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer
from aquarium.models import Aquarium
from consumers.router_message.builders.device_message import set_settings_request
from device.serializers.device import DeviceSerializer
from utils.check_hour_in_range import check_hour_in_range


@shared_task
def check_devices():
    aquariums = Aquarium.objects.all()
    for aquarium in aquariums:
        to_save = []
        if not aquarium.mode:
            continue
        led_mode = check_hour_in_range(aquarium.led_start, aquarium.led_stop)
        fluo_mode = check_hour_in_range(aquarium.fluo_start, aquarium.fluo_stop)
        if led_mode != aquarium.led_mode:
            aquarium.led_mode = led_mode
            to_save.append("led_mode")
        if fluo_mode != aquarium.fluo_mode:
            aquarium.fluo_mode = fluo_mode
            to_save.append("fluo_mode")
        if not to_save:
            continue
        aquarium.save(update_fields=to_save)
        to_device_reqeust = set_settings_request(
            aquarium, {"led_mode": led_mode, "fluo_mode": fluo_mode}
        )
        async_to_sync(get_channel_layer().group_send)(
            f"router_{aquarium.get_router_mac()}",
            {
                "type": "router_send",
                "data": to_device_reqeust.to_json(),
            },
        )

        async_to_sync(get_channel_layer().group_send)(
            f"home_{aquarium.home.id}",
            {
                "type": "send_to_frontend",
                "data": {"status": 200, "data": DeviceSerializer(aquarium).data},
            },
        )
