import pytest
from rest_framework.exceptions import ValidationError
from rfid.serializer import RfidSerializer, CardSerializer, RfidSerializerDevice
from rfid.models import Rfid, Card


@pytest.mark.django_db
def test_rfid_serializer_get_cards(rfid):
    """
    RfidSerializer should return all cards via get_cards()
    """
    card = Card.objects.create(rfid=rfid, name="Test", uid=37123279)

    data = RfidSerializer(rfid).data
    assert "cards" in data
    assert len(data["cards"]) == 1
    assert data["cards"][0]["name"] == card.name


@pytest.mark.django_db
def test_card_serializer_unique_together(rfid):
    """
    Should raise ValidationError if Card with same rfid and name exists
    """
    Card.objects.create(rfid=rfid, name="Card1", uid=712878)

    serializer = CardSerializer(data={"rfid": rfid.id, "name": "Card1"})
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    assert "already exists" in str(excinfo.value)


@pytest.mark.django_db
def test_rfid_serializer_device_only_name(rfid):
    """
    RfidSerializerDevice should serialize only 'name' field
    """
    serializer = RfidSerializerDevice(rfid)
    data = serializer.data
    assert set(data.keys()) == {"name"}
