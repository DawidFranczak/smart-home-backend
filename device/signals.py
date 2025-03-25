from django.dispatch import receiver
from django.db.models.signals import post_migrate

from .models import DeviceSettings

@receiver(post_migrate)
def add_default_values(sender, **kwargs) -> None:
    if not DeviceSettings.objects.filter(fun="aquarium").exists():
        DeviceSettings.objects.create(
            fun="aquarium", message="password_aquarium", answer="respond_aquarium", port=7863
        )
    # if not DeviceSettings.objects.filter(fun="sunblind").exists():
    #     DeviceSettings.objects.create(
    #         fun="sunblind", message="", answer="", port=
    #     )
    # if not DeviceSettings.objects.filter(fun="temp").exists():
    #     DeviceSettings.objects.create(
    #         fun="temp", message="", answer="", port=
    #     )
    # if not DeviceSettings.objects.filter(fun="light").exists():
    #     DeviceSettings.objects.create(
    #         fun="light", message="", answer="", port=
    #     )
    # if not DeviceSettings.objects.filter(fun="stairs").exists():
    #     DeviceSettings.objects.create(
    #         fun="stairs", message="", answer="", port=
    #     )
    if not DeviceSettings.objects.filter(fun="rfid").exists():
        DeviceSettings.objects.create(
            fun="rfid", message="password_rfid", answer="respond_rfid", port=3984
        )
    if not DeviceSettings.objects.filter(fun="button").exists():
        DeviceSettings.objects.create(
            fun="button", message="password_button", answer="respond_button", port=7894
        )
    if not DeviceSettings.objects.filter(fun="lamp").exists():
        DeviceSettings.objects.create(
            fun="lamp", message="password_lamp", answer="respond_lamp", port=4569
        )
    # if not DeviceSettings.objects.filter(fun="uid").exists():
    #     DeviceSettings.objects.create(
    #         fun="uid", message="", answer="", port=
    #     )
    # if not DeviceSettings.objects.filter(fun="").exists():
    #     DeviceSettings.objects.create(
    #         fun="", message="", answer="", port=
    #     )
