import pytest
from unittest.mock import patch

from django.urls import reverse
from device.models import Event


@pytest.mark.django_db
class TestTriggerEventView:
    def test_missing_fields_returns_400(self, auth_client):
        url = reverse("trigger-event")
        response = auth_client.post(url, {})
        assert response.status_code == 400

    @patch("consumers.router_message.builders.basic.get_event_request")
    @patch("consumers.router_message.messenger.DeviceMessenger")
    def test_valid_request_no_events_returns_200(
        self,
        mock_messenger,
        mock_get_event_request,
        auth_client,
        device,
    ):
        url = reverse("trigger-event")
        response = auth_client.post(
            url,
            {"id": device.id, "type": "door_open"},
            format="json",
        )

        assert response.status_code == 200
        mock_messenger.assert_not_called()

    @patch("event.views.DeviceMessenger")
    def test_valid_request_sends_events(
        self, mock_messenger, auth_client, device, lamp
    ):
        Event.objects.create(
            device=device, event="on_click", target_device=lamp, action="on"
        )
        Event.objects.create(
            device=device, event="on_click", target_device=lamp, action="off"
        )

        url = reverse("trigger-event")

        response = auth_client.post(
            url,
            {"id": device.id, "type": "on_click"},
            format="json",
        )

        assert response.status_code == 200

        assert mock_messenger.return_value.send.call_count == 2
