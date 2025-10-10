from datetime import time
import pytest
from unittest.mock import patch, Mock
from aquarium.serializer import AquariumSerializer, AquariumSerializerDevice


@pytest.mark.django_db
def test_validate_led_time_sets_led_mode_true(aquarium, mocker):
    """
    Should set led_mode=True when check_hour_in_range returns True
    """
    mocker.patch("aquarium.serializer.check_hour_in_range", return_value=True)

    serializer = AquariumSerializer(
        instance=aquarium,
        data={
            "led_start": time(10, 0),
            "led_stop": time(12, 0),
        },
        partial=True,
    )

    assert serializer.is_valid(), serializer.errors
    serializer.save()

    aquarium.refresh_from_db()
    assert aquarium.led_mode is True


@pytest.mark.django_db
def test_validate_fluo_lamp_time_sets_fluo_mode_false(aquarium, mocker):
    """
    Should set fluo_mode=False when check_hour_in_range returns False
    """
    mocker.patch("aquarium.serializer.check_hour_in_range", return_value=False)

    serializer = AquariumSerializer(
        instance=aquarium,
        data={
            "fluo_start": time(18, 0),
            "fluo_stop": time(20, 0),
        },
        partial=True,
    )

    assert serializer.is_valid(), serializer.errors
    serializer.save()

    aquarium.refresh_from_db()
    assert aquarium.fluo_mode is False


@pytest.mark.django_db
def test_validate_mode_sets_both_modes(aquarium, mocker):
    """
    Should set both fluo_mode and led_mode during validate_mode()
    """
    mocker.patch("aquarium.serializer.check_hour_in_range", return_value=True)
    serializer = AquariumSerializer(instance=aquarium)
    serializer.validate_mode({})
    assert aquarium.fluo_mode is True
    assert aquarium.led_mode is True


@pytest.mark.django_db
@patch("aquarium.serializer.DeviceMessenger")
@patch("aquarium.serializer.set_settings_request")
def test_update_sends_device_message(mock_set_req, mock_messenger, aquarium):
    """
    update() should call set_settings_request and DeviceMessenger.send()
    """
    mock_request = Mock()
    mock_set_req.return_value = mock_request
    mock_send = Mock()
    mock_messenger.return_value.send = mock_send

    serializer = AquariumSerializer(
        instance=aquarium, data={"color_r": 100}, partial=True
    )
    assert serializer.is_valid()
    serializer.save()

    mock_set_req.assert_called_once()
    mock_send.assert_called_once()


@pytest.mark.django_db
def test_device_serializer_returns_modes_based_on_mode_true(aquarium, mocker):
    """
    AquariumSerializerDevice should recalculate modes if mode=True
    """
    aquarium.mode = True
    mocker.patch("aquarium.serializer.check_hour_in_range", return_value=True)

    serializer = AquariumSerializerDevice(aquarium)
    data = serializer.data

    assert data["led_mode"] is True
    assert data["fluo_mode"] is True


@pytest.mark.django_db
def test_device_serializer_returns_modes_directly_if_mode_false(aquarium, mocker):
    """
    AquariumSerializerDevice should return stored values if mode=False
    """
    aquarium.mode = False
    aquarium.led_mode = False
    aquarium.fluo_mode = True

    serializer = AquariumSerializerDevice(aquarium)
    data = serializer.data

    assert data["led_mode"] is False
    assert data["fluo_mode"] is True
