from datetime import datetime
from datetime import time


def check_hour_in_range(start_hour: time, end_hour: time):
    current = datetime.now().time()
    return (
        current > start_hour or current < end_hour
        if start_hour > end_hour
        else start_hour < current < end_hour
    )
