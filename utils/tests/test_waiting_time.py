import pytest
from unittest.mock import patch
import datetime
from utils.waiting_time import waiting_time


@pytest.mark.parametrize(
    "mock_now,expected_seconds",
    [
        (datetime.datetime(2025, 11, 4, 10, 10), 50 * 60),  # 10:10 → 11:00
        (datetime.datetime(2025, 11, 4, 10, 40), 80 * 60),  # 10:40 → 12:00
        (datetime.datetime(2025, 11, 4, 10, 59), 61 * 60),  # 11:00 → 12:00
        (datetime.datetime(2025, 11, 4, 15, 30), 90 * 60),  # 15:30 → 16:00
        (datetime.datetime(2025, 11, 4, 23, 10), 50 * 60),  # 23:10 → 00:00
        (datetime.datetime(2025, 11, 4, 23, 40), 80 * 60),  # 23:40 → 01:00
        (datetime.datetime(2025, 11, 4, 23, 59), 61 * 60),  # 23:59 → 01:00
        (datetime.datetime(2025, 11, 4, 12, 0), 60 * 60),  # 12:00 → 13:00
    ],
)
def test_waiting_time_returns_expected_seconds(mock_now, expected_seconds):
    with patch("utils.waiting_time.datetime") as mock_dt:
        mock_dt.now.return_value = mock_now
        mock_dt.side_effect = lambda *args, **kwargs: datetime.datetime(*args, **kwargs)

        result = waiting_time()
        seconds = round(result)
        assert (
            seconds == expected_seconds
        ), f"For {mock_now}, expected {expected_seconds}, got {seconds}"
