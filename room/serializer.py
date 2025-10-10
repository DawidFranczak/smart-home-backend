from rest_framework import serializers
from django.utils import timezone

from device.serializers.device import DeviceSerializer
from .models import Room


class RoomSerializer(serializers.ModelSerializer):
    device_count = serializers.SerializerMethodField()
    active_device_count = serializers.SerializerMethodField()
    device = serializers.PrimaryKeyRelatedField(
        source="devices",
        many=True,
        read_only=True,
    )
    is_favourite = serializers.SerializerMethodField()

    def get_is_favourite(self, object: Room) -> bool:
        user = object.user
        return user.favourite.room.filter(pk=object.id).exists()

    def get_device_count(self, object: Room) -> int:
        return object.devices.count()

    def get_active_device_count(self, object: Room) -> int:
        time_threshold = timezone.now() - timezone.timedelta(minutes=10)
        return object.devices.filter(last_seen__gt=time_threshold).count()

    class Meta:
        model = Room
        fields = [
            "id",
            "name",
            "visibility",
            "device_count",
            "active_device_count",
            "is_favourite",
            "device",
        ]
        read_only_fields = ["home", "user"]

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep["visibility"] = instance.get_visibility_display()
        return rep

    def to_internal_value(self, data):
        visibility_map = {
            "public": Room.Visibility.PUBLIC,
            "private": Room.Visibility.PRIVATE,
        }
        if "visibility" in data:
            data["visibility"] = visibility_map.get(
                data["visibility"].lower(), data["visibility"]
            )
        return super().to_internal_value(data)

    def validate_visibility(self, value) -> Room.Visibility:
        if value not in [Room.Visibility.PUBLIC, Room.Visibility.PRIVATE]:
            raise serializers.ValidationError("Invalid visibility value")
        print(value)
        return value

    def validate_name(self, value):
        view = self.context.get("view")
        queryset = view.get_queryset()
        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters long")
        if any(room.name == value for room in queryset):
            raise serializers.ValidationError("Room with this name already exists")
        return value
