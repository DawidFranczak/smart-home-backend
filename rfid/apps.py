from django.apps import AppConfig

from device_registry import DeviceRegistry


class RfidConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "rfid"

    def ready(self):
        from .models import Rfid
        from .serializer import RfidSerializer, RfidSerializerDevice

        registry = DeviceRegistry()
        registry.register_device("rfid", Rfid, RfidSerializer, RfidSerializerDevice)
