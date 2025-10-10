from django.apps import AppConfig

from device_registry import DeviceRegistry


class LampConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "lamp"

    def ready(self):
        from .models import Lamp
        from .serializer import LampSerializer, LampSerializerDevice

        registry = DeviceRegistry()
        registry.register_device("lamp", Lamp, LampSerializer, LampSerializerDevice)
