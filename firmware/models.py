from django.db import models

# Create your models here.


class FirmwareDevice(models.Model):
    version = models.FloatField()
    to_device = models.CharField(max_length=100)
    file = models.FileField(upload_to="firmware_device/")
    created_at = models.DateTimeField(auto_now_add=True)
