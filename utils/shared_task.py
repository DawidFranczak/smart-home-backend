from celery import shared_task

from consumers.communication_protocol.message_event import MessageEvent
from rfid.models import Rfid
from utils.web_socket_message import update_frontend_device


@shared_task
def check_add_card_request(rfid_id):
    try:
        rfid = Rfid.objects.get(id=rfid_id)
    except Rfid.DoesNotExist:
        return
    if not MessageEvent.ADD_TAG.value in rfid.pending:
        return
    try:
        rfid.pending.remove(MessageEvent.ADD_TAG.value)
    except ValueError:
        return
    rfid.save(update_fields=["pending"])
    update_frontend_device(rfid, 404)
