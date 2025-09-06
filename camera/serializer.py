from rest_framework.serializers import ModelSerializer, UniqueTogetherValidator, PrimaryKeyRelatedField, IPAddressField
from camera.models import Camera

from user.models import Home

class CameraSerializer(ModelSerializer):
    home = PrimaryKeyRelatedField(queryset=Home.objects.all(),write_only=True)
    ip_address = IPAddressField(write_only=True)

    class Meta:
        model = Camera
        fields = ["id", "name", "home", "ip_address"]
        validators = [
            UniqueTogetherValidator(
                queryset=Camera.objects.all(),
                fields=["name", "home"],
                message="Camera with this name already exists."
            ),
            UniqueTogetherValidator(
                queryset=Camera.objects.all(),
                fields=["ip_address", "home"],
                message="Camera with this ip already exists."
            )
        ]