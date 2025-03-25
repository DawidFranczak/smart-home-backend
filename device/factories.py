from aquarium.models import Aquarium
from lamp.models import Lamp
from button.models import Button
from rfid.models import Rfid, Card
from stairs.models import Stairs
from temperature.models import TemperatureSensor
from sunblind.models import Sunblind
from light.models import Light


def create_device(
    data,
) -> (
    TemperatureSensor
    | Sunblind
    | Aquarium
    | Stairs
    | Rfid
    | Card
    | Button
    | Light
    | Lamp
):
    if data["fun"] == "aquarium":
        return Aquarium.objects.create(**data)
    elif data["fun"] == "rfid":
        return Rfid.objects.create(**data)
    elif data["fun"] == "button":
        return Button.objects.create(**data)
    elif data["fun"] == "lamp":
        return Lamp.objects.create(**data)
    else:
        raise ValueError(f"Unknown function type: {data["fun"]}")

    # elif data["fun"] == "stairs":
    #     return Stairs.objects.create(sensor=sensor)
    # if data["fun"] == "temperature":
    #     return Temp.objects.create(sensor=sensor, time=datetime.now(), temp=0.0, humi=0.0)
    # elif data["fun"] == "sunblind":
    #     return Sunblind.objects.create(sensor=sensor)
