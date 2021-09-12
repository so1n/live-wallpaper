import datetime
import time


def now_tz() -> datetime.timezone:
    return datetime.timezone(datetime.timedelta(seconds=-time.altzone))


def calculate_time_offset(latest_date: datetime.datetime, offset: int) -> datetime.datetime:
    offset_time = latest_date + datetime.timedelta(hours=offset)
    return offset_time
