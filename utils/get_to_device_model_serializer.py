from aquarium.models import Aquarium
from aquarium.serializer import AquariumSerializerDevice


def get_to_device_model_serializer(fun: str):
    serializers = {"aquarium": (Aquarium, AquariumSerializerDevice)}
    if not fun in serializers:
        return None, None
    return serializers[fun]
