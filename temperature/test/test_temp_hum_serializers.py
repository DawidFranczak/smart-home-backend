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
def test_sleeping_time(mock_now, expected_delta_hours, temp_hum):
    serializer = TempHumSerializerDevice(instance=temp_hum)

    with patch("utils.sleeping_time.datetime.datetime") as mock_datetime, patch(
        "utils.sleeping_time.time"
    ) as mock_time:
        mock_datetime.now.return_value = mock_now
        mock_datetime.side_effect = lambda *args, **kwargs: datetime(*args, **kwargs)
        mock_time.time.return_value = mock_now.timestamp()

        sleeping_ms = serializer.get_sleeping_time(temp_hum)
        # convert ms to hours
        sleeping_hours = sleeping_ms / (1000 * 60 * 60)
        assert isinstance(sleeping_ms, int)
        # Allow small delta for computation rounding
        assert abs(sleeping_hours - expected_delta_hours) < 2
