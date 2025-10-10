from utils.check_hour_in_range import check_hour_in_range
from datetime import time, datetime


def test_time_within_range(mocker):
    """
    Test case: current time is within the range (normal range, same day)
    """
    # Mock datetime class
    mock_datetime = mocker.Mock(wraps=datetime)
    mock_datetime.now.return_value = datetime(2025, 10, 11, 10, 30)  # 10:30

    # Patch datetime in the module
    mocker.patch("utils.check_hour_in_range.datetime", mock_datetime)

    start = time(10, 0)
    end = time(11, 0)

    result = check_hour_in_range(start, end)
    assert result is True


def test_time_outside_range(mocker):
    """
    Test case: current time is outside the range (normal range, same day)
    """
    mock_datetime = mocker.Mock(wraps=datetime)
    mock_datetime.now.return_value = datetime(2025, 10, 11, 12, 0)  # 12:00

    mocker.patch("utils.check_hour_in_range.datetime", mock_datetime)

    start = time(10, 0)
    end = time(11, 0)

    result = check_hour_in_range(start, end)
    assert result is False


def test_time_cross_midnight_in_range(mocker):
    """
    Test case: range crosses midnight, current time is within the range
    """
    mock_datetime = mocker.Mock(wraps=datetime)
    mock_datetime.now.return_value = datetime(2025, 10, 11, 1, 0)  # 01:00

    mocker.patch("utils.check_hour_in_range.datetime", mock_datetime)

    start = time(23, 0)
    end = time(2, 0)  # crosses midnight

    result = check_hour_in_range(start, end)
    assert result is True


def test_time_cross_midnight_outside_range(mocker):
    """
    Test case: range crosses midnight, current time is outside the range
    """
    mock_datetime = mocker.Mock(wraps=datetime)
    mock_datetime.now.return_value = datetime(2025, 10, 11, 3, 0)  # 03:00

    mocker.patch("utils.check_hour_in_range.datetime", mock_datetime)

    start = time(23, 0)
    end = time(2, 0)  # crosses midnight

    result = check_hour_in_range(start, end)
    assert result is False
