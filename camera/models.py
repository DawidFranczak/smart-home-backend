from django.db import models
from user.models import Home

class Camera(models.Model):
    home = models.ForeignKey(Home, on_delete=models.CASCADE, related_name="cameras")
    name = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField()
    port = models.PositiveIntegerField(default=554)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name