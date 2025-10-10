import pytest
from button.serializer import ButtonSerializer, ButtonSerializerDevice


@pytest.mark.django_db
def test_button_serializer_excludes_mac_field(button):
    """
    ButtonSerializer should exclude the 'mac' field
    """
    serializer = ButtonSerializer(button)
    data = serializer.data
    assert "mac" not in data
    assert "name" in data


@pytest.mark.django_db
def test_button_serializer_device_includes_only_name(button):
    """
    ButtonSerializerDevice should only include the 'name' field
    """
    serializer = ButtonSerializerDevice(button)
    data = serializer.data
    assert list(data.keys()) == ["name"]
