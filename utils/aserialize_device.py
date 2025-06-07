from asgiref.sync import sync_to_async


@sync_to_async
def aserialize_device(device):
    from device.serializers.device import DeviceSerializer

    return DeviceSerializer(device).data
