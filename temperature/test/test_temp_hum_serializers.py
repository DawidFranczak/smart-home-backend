from datetime import datetime
from unittest.mock import patch

import pytest

from temperature.serializer import TempHumSerializerDevice


@pytest.mark.parametrize(
    "mock_now, expected_delta_hours",
    [
        (datetime(2025, 10, 11, 10, 15), 1),  # minute <= 30
        (datetime(2025, 10, 11, 10, 45), 2),  # minute > 30
    ],
)
def test_waiting_time(mock_now, expected_delta_hours, temp_hum):
    serializer = TempHumSerializerDevice(instance=temp_hum)

    with patch("utils.waiting_time.datetime") as mock_datetime:
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)

        sleeping_ms = serializer.get_waiting_time(temp_hum)
        # convert ms to hours
        sleeping_hours = sleeping_ms / (1000 * 60 * 60)
        assert isinstance(sleeping_ms, int)
        # Allow small delta for computation rounding
        assert abs(sleeping_hours - expected_delta_hours) < 2
