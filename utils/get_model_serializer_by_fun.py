from aquarium.serializer import AquariumSerializer
from button.serializer import ButtonSerializer
from light.serializer import LightSerializer
from lamp.serializer import LampSerializer
from rfid.serializer import RfidSerializer
from sunblind.serializer import SunblindSerializer
from stairs.serializer import StairsSerializer
from temperature.serializer import TemperatureSerializer
from temperature.models import TemperatureSensor
from sunblind.models import Sunblind
from aquarium.models import Aquarium
from stairs.models import Stairs
from lamp.models import Lamp
from rfid.models import Rfid
from button.models import Button
from light.models import Light


def get_model_serializer_by_fun(fun: str):
    device_type_map = {
        "temperature": (TemperatureSensor, TemperatureSerializer),
        "sunblind": (Sunblind, SunblindSerializer),
        "aquarium": (Aquarium, AquariumSerializer),
        "stairs": (Stairs, StairsSerializer),
        "lamp": (Lamp, LampSerializer),
        "rfid": (Rfid, RfidSerializer),
        "button": (Button, ButtonSerializer),
        "light": (Light, LightSerializer),
    }
    if fun not in device_type_map:
        return None, None
    return device_type_map[fun]
