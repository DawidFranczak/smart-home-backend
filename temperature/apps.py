from django.apps import AppConfig


class TemperatureConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'temperature'

    def ready(self):
        from device_registry import DeviceRegistry
        from temperature.models import TempHum
        from temperature.serializer import TempHumSerializer, TempHumSerializerDevice

        device_register = DeviceRegistry()
        device_register.register_device(
            "temp_hum",
            TempHum,
            TempHumSerializer,
            TempHumSerializerDevice
        )