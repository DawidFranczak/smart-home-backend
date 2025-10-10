from django.apps import AppConfig
from device_registry import DeviceRegistry


class AquariumConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "aquarium"

    def ready(self):
        from .models import Aquarium
        from .serializer import AquariumSerializer
        from .serializer import AquariumSerializerDevice

        registry = DeviceRegistry()
        registry.register_device(
            "aquarium", Aquarium, AquariumSerializer, AquariumSerializerDevice
        )
