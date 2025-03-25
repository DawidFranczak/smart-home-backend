from turtle import home

from django.db.models import JSONField
from django.utils import timezone
from django.db import models

from room.models import Room
from user.models import Home


class DeviceSettings(models.Model):
    fun = models.CharField(max_length=100, default="")
    message = models.CharField(max_length=100, default="")
    answer = models.CharField(max_length=100, default="")
    port = models.IntegerField()

    def __str__(self) -> str:
        return self.fun


class Router(models.Model):
    ip = models.CharField(max_length=100, default="")
    mac = models.CharField(max_length=100)
    home = models.OneToOneField(Home, on_delete=models.CASCADE, related_name="router")
    wifi_strength = models.IntegerField(default=0)
    last_seen = models.DateTimeField(auto_now=True)
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return self.mac


class Device(models.Model):
    room = models.ForeignKey(
        Room, on_delete=models.SET_NULL, related_name="devices", null=True, default=None
    )
    home = models.ForeignKey(
        Home, on_delete=models.CASCADE, related_name="devices", null=True
    )
    name = models.CharField(max_length=100, default="Nieznane")
    ip = models.CharField(max_length=100)
    port = models.IntegerField()
    fun = models.CharField(max_length=100, default="")
    last_seen = models.DateTimeField(auto_created=True)
    mac = models.CharField(max_length=100, default="")
    wifi_strength = models.IntegerField(default=0)
    pending = JSONField(default=list, blank=True)

    def __str__(self):
        return self.name

    def get_router(self):
        return Router.objects.get(home=self.home)

    def get_router_mac(self):
        return Router.objects.filter(home=self.home).only("mac").first()


class Event(models.Model):
    device = models.ForeignKey(Device, on_delete=models.CASCADE)
    message = models.CharField(max_length=40)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.device} - {self.message} - {self.date}"
