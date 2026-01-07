from django.apps import AppConfig

from consumers.router_message.message_event import MessageEvent
from device_registry import DeviceRegistry


class LightConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "light"

    def ready(self):
        from .models import Light
        from .serializer import LightSerializerDevice, LightSerializer

        registry = DeviceRegistry()
        registry.register_device(
            "light",
            Light,
            LightSerializer,
            LightSerializerDevice,
            [MessageEvent.ON.value, MessageEvent.OFF.value],
        )
