import pytest
from unittest.mock import patch, MagicMock
from rest_framework.exceptions import ValidationError

from device.serializers.device import DeviceSerializer
from device.models import Device



@pytest.mark.django_db
def test_is_favourite(aquarium):
    serializer = DeviceSerializer()
    assert serializer.get_is_favourite(aquarium) is False


@pytest.mark.django_db
def test_is_favourite_true(user, room, device):
    user.favourite.device.add(device)
    serializer = DeviceSerializer()
    assert serializer.get_is_favourite(device) is True


@pytest.mark.django_db
def test_get_device_serializer_missing_fun(device):
    device.fun = ""
    serializer = DeviceSerializer()
    with pytest.raises(ValidationError):
        serializer._get_device_serializer(device)


@pytest.mark.django_db
def test_get_device_serializer_invalid_fun(device, mocker):
    device.fun = "invalid"
    serializer = DeviceSerializer()
    mocker.patch("device.serializers.device.DeviceRegistry.get_model", return_value=None)
    mocker.patch("device.serializers.device.DeviceRegistry.get_serializer", return_value=None)

    with pytest.raises(ValidationError):
        serializer._get_device_serializer(device)


@pytest.mark.django_db
def test_to_representation_calls_nested_serializer(mocker, device):
    serializer_class = MagicMock()
    serializer_class.return_value.data = {"extra": "data"}
    mocker.patch("device.serializers.device.DeviceRegistry.get_model", return_value=Device)
    mocker.patch("device.serializers.device.DeviceRegistry.get_serializer", return_value=serializer_class)
    mocker.patch("event.serializer.EventSerializer", return_value=MagicMock(data=[{"event": "E1"}]))

    serializer = DeviceSerializer()
    result = serializer.to_representation(device)

    assert "extra" in result
    assert "events" in result


@pytest.mark.django_db
def test_update_calls_nested_serializer(mocker, device):
    mock_serializer = MagicMock()
    mock_serializer.is_valid.return_value = True
    mock_serializer.save.return_value = device
    mocker.patch("device.serializers.device.DeviceRegistry.get_model", return_value=Device)
    mocker.patch("device.serializers.device.DeviceRegistry.get_serializer",return_value=lambda *args, **kwargs: mock_serializer)
    mocker.patch("device.serializers.device.update_frontend_device")

    serializer = DeviceSerializer(instance=device, data={"name": "New"}, partial=True)
    serializer.is_valid()
    result = serializer.update(device, {"name": "New"})

    assert result == device
    assert mock_serializer.is_valid.called
    assert mock_serializer.save.called


# @pytest.mark.django_db
# def test_create_calls_nested_serializer(mocker, device):
#     mock_serializer = MagicMock()
#     mock_serializer.is_valid.return_value = True
#     mock_serializer.save.return_value = device
#     mocker.patch("device.serializers.device.DeviceRegistry.get_model", return_value=Device)
#     mocker.patch("device.serializers.device.DeviceRegistry.get_serializer", return_value=lambda fun: mock_serializer)
#
#     serializer = DeviceSerializer(data={"name": "DeviceX"})
#     serializer.is_valid()
#     result = serializer.create({"fun": device.fun})
#
#     assert result == device
#     assert mock_serializer.is_valid.called
#     assert mock_serializer.save.called
