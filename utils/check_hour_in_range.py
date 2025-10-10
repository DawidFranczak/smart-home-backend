from datetime import datetime
from datetime import time


def check_hour_in_range(start_hour: time, end_hour: time) -> bool:
    """
    Check if the current time is within a specified range.

    Handles ranges that cross midnight.

    Args:
        start_hour (time): Start of the range.
        end_hour (time): End of the range.

    Returns:
        bool: True if current time is within the range, False otherwise.
    """
    current = datetime.now().time()
    return (
        current > start_hour or current < end_hour
        if start_hour > end_hour
        else start_hour < current < end_hour
    )
