from django.db import models
from django.contrib.auth.models import User
from user.models import Home


class Room(models.Model):
    class Visibility(models.TextChoices):
        PRIVATE = "PR", "private"
        PUBLIC = "PU", "public"

    name = models.CharField(max_length=100, default="")
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="rooms")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_rooms")
    visibility = models.CharField(
        max_length=2, choices=Visibility.choices, default=Visibility.PUBLIC
    )

    def __str__(self):
        return self.name
