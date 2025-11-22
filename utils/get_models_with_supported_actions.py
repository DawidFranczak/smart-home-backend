from django.apps import apps
from django.core.cache import cache
from django.contrib.auth.models import User
from device.models import Device


def get_models_with_supported_actions(user: User):
    # cache_key = "models_with_actions"
    # supported_models = cache.get(cache_key)
    # if supported_models is None:
    supported_models = []
    for model in apps.get_models():
        if not issubclass(model, Device) or model is Device:
            continue
        instance = model.objects.filter(home__users=user).only("id").first()
        if instance and instance.available_actions():
            supported_models.append(model.__name__)
    # cache.set(cache_key, supported_models, 60 * 60 * 24)

    return supported_models
