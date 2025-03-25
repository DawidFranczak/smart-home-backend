from asgiref.sync import  async_to_sync
from celery import shared_task
from channels.layers import get_channel_layer

from aquarium.command import check_and_change_led_time_request, check_and_change_fluo_lamp_time_request
from aquarium.models import Aquarium


@shared_task
def check_devices():
    aquariums = Aquarium.objects.all()
    for aquarium in aquariums:
        to_save = []
        if not aquarium.mode:
            continue
        led_result = check_and_change_led_time_request(aquarium, aquarium.led_start, aquarium.led_stop)
        if led_result != aquarium.led_mode:
            aquarium.led_mode = led_result
            to_save.append("led_mode")
        fluo_result = check_and_change_fluo_lamp_time_request(aquarium, aquarium.fluo_start, aquarium.fluo_stop)
        if fluo_result != aquarium.fluo_mode:
            aquarium.fluo_mode = fluo_result
            to_save.append("fluo_mode")
        if to_save:
            aquarium.save(update_fields=to_save)
