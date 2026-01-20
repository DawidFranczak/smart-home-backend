from django.apps import AppConfig


class StairsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "stairs"

    def ready(self):
        from .models import Stairs
        from .serializer import StairsSerializer, StairsSerializerDevice
        from device_registry import DeviceRegistry

        DeviceRegistry().register_device(
            "stairs", Stairs, StairsSerializer, StairsSerializerDevice
        )
