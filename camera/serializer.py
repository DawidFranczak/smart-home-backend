from rest_framework import serializers
from camera.models import Camera

class CameraReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camera
        fields = ["id","name"]

class CameraWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Camera
        fields = "__all__"
        # validators = [
        #     serializers.UniqueTogetherValidator(
        #         queryset=Camera.objects.all(),
        #         fields=["ip_address", "home"],
        #         message="Camera with this ip already exists."
        #     ),
        #     serializers.UniqueTogetherValidator(
        #         queryset=Camera.objects.all(),
        #         fields=["name", "home"],
        #         message="Camera with this name already exists."
        #     ),
        # ]

    def validate(self, attrs):
        home = attrs.get("home")
        name = attrs.get("name")
        ip_address = attrs.get("ip_address")

        if Camera.objects.filter(home=home, name=name).exists():
            raise serializers.ValidationError({"name": "Camera with this name already exists."})

        if Camera.objects.filter(home=home, ip_address=ip_address).exists():
            raise serializers.ValidationError({"ip_address": "Camera with this IP already exists."})

        return attrs