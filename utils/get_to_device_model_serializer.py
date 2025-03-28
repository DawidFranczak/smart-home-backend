from aquarium.models import Aquarium
from aquarium.serializer import AquariumSerializerDevice
from rfid.models import Rfid
from rfid.serializer import RfidSerializerDevice


def get_to_device_model_serializer(fun: str):
    serializers = {
        "aquarium": (Aquarium, AquariumSerializerDevice),
        "rfid": (Rfid, RfidSerializerDevice),
    }
    if not fun in serializers:
        return None, None
    return serializers[fun]
