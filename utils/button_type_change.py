from button.models import ButtonType
from consumers.router_message.message_event import MessageEvent
from device.models import Event


def button_type_change(new_button_type: str, instance):
    if new_button_type == instance.button_type:
        return
    event_filter = (
        [MessageEvent.ON_CLICK.value, MessageEvent.ON_HOLD.value]
        if instance.button_type == ButtonType.MONOSTABLE
        else [MessageEvent.ON_TOGGLE]
    )
    Event.objects.filter(device=instance, event__in=event_filter).delete()
