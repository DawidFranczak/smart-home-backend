import pytest
from unittest.mock import Mock, patch
from consumers.events.add_tag import AddTagEvent
from consumers.router_message.device_message import DeviceMessage
from rfid.models import Rfid, Card


@pytest.mark.django_db
def test_handle_response_no_uid(room, home, rfid):
    """If UID is None, the method should do nothing."""
    event = AddTagEvent()
    message = Mock(spec=DeviceMessage)
    message.payload = Mock()
    message.payload.uid = None
    message.payload.name = "Test Card"
    message.device_id = rfid.id

    result = event.handle_response(Mock(), message)
    assert result is None


@pytest.mark.django_db
def test_handle_response_device_not_found(room, home, rfid):
    """If the device is not found, the method should do nothing."""
    event = AddTagEvent()
    message = Mock(spec=DeviceMessage)
    message.payload = Mock()
    message.payload.uid = "123456"
    message.payload.name = "Test Card"
    message.device_id = 999999  # non-existent ID

    # Mock _get_device to return None
    event._get_device = Mock(return_value=None)

    result = event.handle_response(Mock(), message)
    assert result is None


@pytest.mark.django_db
@patch("consumers.events.add_tag.FrontendMessenger")
def test_handle_response_creates_card(mock_frontend, room, home, rfid):
    """Creates a new card if UID does not exist."""
    event = AddTagEvent()
    message = Mock(spec=DeviceMessage)
    message.payload = Mock()
    message.payload.uid = "123456"
    message.payload.name = "Test Card"
    message.device_id = rfid.id

    event._get_device = Mock(return_value=rfid)

    # Ensure the Card does not exist yet
    assert not Card.objects.filter(uid="123456").exists()

    event.handle_response(Mock(), message)

    card = Card.objects.get(uid="123456")
    assert card.rfid == rfid
    assert card.name == "Test Card"
    assert "ADD_TAG" not in rfid.pending

    # Check FrontendMessenger was called correctly
    mock_frontend.return_value.update_frontend.assert_called_once()
    args, kwargs = mock_frontend.return_value.update_frontend.call_args
    assert args[0] == rfid.home.id
    assert args[2] == 201  # "created" status


@pytest.mark.django_db
@patch("consumers.events.add_tag.FrontendMessenger")
def test_handle_response_card_exists(mock_frontend, room, home, rfid):
    """If the card already exists, it should not create a new one, and return 409."""
    event = AddTagEvent()
    message = Mock(spec=DeviceMessage)
    message.payload = Mock()
    message.payload.uid = "123456"
    message.payload.name = "Existing Card"
    message.device_id = rfid.id

    event._get_device = Mock(return_value=rfid)

    # Create an existing Card
    Card.objects.create(uid="123456", rfid=rfid, name="Old Card")

    event.handle_response(Mock(), message)

    # Ensure no new card is created
    cards = Card.objects.filter(uid="123456")
    assert cards.count() == 1

    # Status 409 should be sent to FrontendMessenger
    mock_frontend.return_value.update_frontend.assert_called_once()
    args, kwargs = mock_frontend.return_value.update_frontend.call_args
    assert args[2] == 409
