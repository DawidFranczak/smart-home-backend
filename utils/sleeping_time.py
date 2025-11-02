import time
import datetime


def waiting_time():
    """Calculate sleeping time for next measurement"""
    now = datetime.datetime.now()
    timestamp = time.time()
    current_hour = now.hour
    if now.minute > 30:
        current_hour += 1
    current_hour += 1

    # Time in timestamp
    next_measured_time = time.mktime(
        now.replace(hour=current_hour, minute=0, second=0, microsecond=0).timetuple()
    )
    return int(next_measured_time - timestamp)
