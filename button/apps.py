from django.apps import AppConfig

from device_registry import DeviceRegistry


class ButtonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "button"

    def ready(self):
        from .models import Button
        from .serializer import ButtonSerializer, ButtonSerializerDevice

        registry = DeviceRegistry()
        registry.register_device(
            "button", Button, ButtonSerializer, ButtonSerializerDevice
        )
