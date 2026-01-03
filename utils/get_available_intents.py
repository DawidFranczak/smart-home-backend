from django.db.models import QuerySet
from django.contrib.auth.models import User
from django.core.cache import cache
from device.models import Device
from device_registry import DeviceRegistry


def get_available_intent(user_id: int, devices: QuerySet[Device]) -> list[str]:
    cache_key = f"available_intent_{user_id}"
    if cache.get(cache_key):
        return cache.get(cache_key)
    intents = set()
    device_registry = DeviceRegistry()
    for device in devices:
        intents.update(device_registry.get_available_intents(device.fun))
    cache.set(cache_key, list(intents), 300)
    return list(intents)
