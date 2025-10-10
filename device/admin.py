from django.contrib import admin

from .models import Device, DeviceSettings, Event, Router

# Register your models here.

admin.site.register(DeviceSettings)
admin.site.register(Device)
admin.site.register(Router)
admin.site.register(Event)
