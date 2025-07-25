from django.apps import apps
from django.core.cache import cache
from django.contrib.auth.models import User
from device.models import Device


def get_models_with_supported_actions(user: User):
    # cache_key = "models_with_actions"
    # supported_models = cache.get(cache_key)
    # if supported_models is None:
    device_models = [model for model in apps.get_models() if issubclass(model, Device)]
    supported_models = [
        model.__name__
        for model in device_models
        if model.objects.filter(home__users=user).exists() and model.available_actions()
    ]
    # cache.set(cache_key, supported_models, 60 * 60 * 24)

    return supported_models
