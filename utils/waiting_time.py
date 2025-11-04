from datetime import datetime, timedelta


def waiting_time():
    """Calculate sleeping time for next measurement"""
    now = datetime.now()
    rounded = now.replace(minute=0, second=0, microsecond=0)
    if now.minute >= 30:
        rounded += timedelta(hours=1)
    next_measure_time = rounded + timedelta(hours=1)
    return int((next_measure_time - now).total_seconds())
