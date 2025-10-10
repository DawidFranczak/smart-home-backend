import pytest
from unittest.mock import patch
from lamp.serializer import LampSerializer, LampSerializerDevice
from lamp.models import Lamp


@pytest.mark.django_db
def test_lamp_serializer_device_fields(lamp):
    """
    LampSerializerDevice should include only brightness, step, lighting_time
    """
    serializer = LampSerializerDevice(lamp)
    data = serializer.data
    assert set(data.keys()) == {"brightness", "step", "lighting_time"}


@pytest.mark.django_db
@patch("lamp.serializer.DeviceMessenger")
@patch("lamp.serializer.set_settings_request")
def test_lamp_serializer_update_calls_messenger(
    mock_set_req, mock_messenger, lamp, mocker
):
    """
    update() should call set_settings_request and DeviceMessenger.send
    """
    mock_request = mocker.Mock()
    mock_set_req.return_value = mock_request
    mock_send = mocker.Mock()
    mock_messenger.return_value.send = mock_send

    serializer = LampSerializer(instance=lamp, data={"brightness": 50}, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()

    mock_set_req.assert_called_once_with(lamp.mac, LampSerializerDevice(lamp).data)
    mock_send.assert_called_once_with(lamp.get_router_mac(), mock_request)


@pytest.mark.django_db
def test_lamp_serializer_update_changes_instance(lamp):
    """
    update() should update lamp instance fields
    """
    serializer = LampSerializer(instance=lamp, data={"brightness": 70}, partial=True)
    serializer.is_valid(raise_exception=True)
    updated_instance = serializer.save()
    lamp.refresh_from_db()
    assert lamp.brightness == 70
    assert updated_instance == lamp
