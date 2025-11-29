import pytest
from unittest.mock import patch, MagicMock

from django.urls import reverse

from device.models import Event


@pytest.mark.django_db
class TestCreateDeleteEvent:

    @patch("event.views.FrontendMessenger")
    @patch("event.views.DeviceRegistry")
    def test_create_event_success(
        self, mock_registry, mock_frontend, auth_client, button, lamp
    ):
        model_mock = MagicMock()
        model_instance = MagicMock()
        model_instance.extra_settings.return_value = {"speed": 1}
        model_mock.objects.get.return_value = model_instance
        mock_registry.return_value.get_model.return_value = model_mock

        url = reverse("event-create-delete", kwargs={"pk": button.id})
        response = auth_client.post(
            url,
            {
                "device": button.id,
                "target_device": lamp.id,
                "action": "turn_on",
                "event": "motion",
                "extra_settings": {"speed": 1},
            },
            format="json",
        )

        assert response.status_code == 201
        assert Event.objects.count() == 1
        mock_frontend.return_value.update_frontend.assert_called_once()

    @patch("device_registry.DeviceRegistry")
    def test_create_event_invalid_extra_settings(
        self, mock_registry, auth_client, button, lamp
    ):
        model_mock = MagicMock()
        model_instance = MagicMock()
        model_instance.extra_settings.return_value = {"brightness": 1}
        model_mock.objects.get.return_value = model_instance
        mock_registry.return_value.get_model.return_value = model_mock

        url = reverse("event-create-delete", kwargs={"pk": button.id})

        response = auth_client.post(
            url,
            {
                "device": button.id,
                "target_device": lamp.id,
                "action": "turn_on",
                "event": "motion",
                "extra_settings": {"invalid_key": 1},
            },
            format="json",
        )

        assert response.status_code == 400
        assert Event.objects.count() == 0

    def test_delete_event(self, auth_client, button, lamp):
        e = Event.objects.create(
            device=button,
            target_device=lamp,
            action="turn_on",
            event="motion",
            extra_settings={},
        )

        url = reverse("event-create-delete", kwargs={"pk": e.pk})

        response = auth_client.delete(url)
        assert response.status_code == 200
        assert Event.objects.count() == 0
