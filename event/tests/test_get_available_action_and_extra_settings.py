import pytest
from unittest.mock import patch, MagicMock

from django.urls import reverse


@pytest.mark.django_db
class TestGetAvailableActionAndExtraSettings:

    @patch("event.views.DeviceRegistry")
    def test_get_actions_and_settings_success(self, mock_registry, auth_client, device):
        model_mock = MagicMock()
        instance = MagicMock()
        instance.available_actions.return_value = ["turn_on"]
        instance.extra_settings.return_value = {"speed": 1}
        model_mock.objects.filter.return_value.first.return_value = instance
        mock_registry().get_model.return_value = model_mock

        url = reverse("available-actions") + "?function=lamp"

        response = auth_client.get(url)

        assert response.status_code == 200
        assert response.data["actions"] == ["turn_on"]
        assert response.data["settings"] == {"speed": 1}

    @patch("event.views.DeviceRegistry")
    def test_invalid_function_returns_404(self, mock_registry, auth_client):
        mock_registry().get_model.return_value = None

        url = reverse("available-actions") + "?function=unknown"

        response = auth_client.get(url)

        assert response.status_code == 404
        assert response.data == []
