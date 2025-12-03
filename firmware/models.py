from django.db import models


class FirmwareDevice(models.Model):
    version = models.FloatField()
    to_device = models.CharField(max_length=100)
    file = models.FileField(upload_to="firmware_device/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.to_device}_{self.version}"
