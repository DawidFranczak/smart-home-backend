from uuid import uuid4
from django.db import models
from django.contrib.auth.models import User


class Home(models.Model):
    users = models.ManyToManyField(User, related_name="home")
    add_uid = models.UUIDField(default=uuid4())


class Favourite(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    device = models.ManyToManyField("device.Device")
    room = models.ManyToManyField("room.Room")

    def __str__(self):
        return self.user.username
