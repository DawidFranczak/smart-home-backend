import pytest
from django.urls import reverse
from unittest.mock import patch
from rfid.models import Rfid, Card
from device.serializers.device import DeviceSerializer


@pytest.mark.django_db
def test_rfid_list_create(auth_client, rfid):
    url = reverse("rfid-list-create")
    response = auth_client.get(url)
    assert response.status_code == 200
    assert len(response.data) >= 1
    assert response.data[0]["id"] == rfid.id


@pytest.mark.django_db
@patch("rfid.views.DeviceMessenger")
@patch("rfid.views.add_tag_request")
@patch("rfid.views.check_add_card_request")
def test_card_list_create(
    mock_task, mock_add_request, mock_messenger, auth_client, rfid
):
    url = reverse("card-list-create")
    data = {"rfid": rfid.id, "name": "TestCard"}

    mock_add_request.return_value = "request_obj"
    mock_messenger.return_value.send = lambda *a, **kw: None
    mock_task.apply_async.return_value = None

    response = auth_client.post(url, data)
    assert response.status_code == 200
    assert "id" in response.data
    rfid.refresh_from_db()
    assert "add_tag" in rfid.pending


@pytest.mark.django_db
@patch("rfid.views.FrontendMessenger")
def test_card_destroy(mock_frontend, auth_client, rfid):
    card = Card.objects.create(rfid=rfid, name="Test", uid=12367)
    url = reverse("card-destroy", args=[card.id])
    mock_frontend.return_value.update_frontend = lambda *a, **kw: None

    response = auth_client.delete(url)
    assert response.status_code == 204
    assert not Card.objects.filter(id=card.id).exists()
