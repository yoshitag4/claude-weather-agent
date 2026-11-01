from datetime import datetime
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def get_current_datetime(date_format="%Y-%m-%d %H:%M:%S", timezone=None):
    """
    Returns the current date and time
    formatted according to the supplied format,
    for the given IANA timezone (e.g. "America/New_York").
    Falls back to the system's local timezone when none is supplied.
    """

    if not timezone:
        return datetime.now().strftime(date_format)

    try:
        now = datetime.now(ZoneInfo(timezone))
    except ZoneInfoNotFoundError:
        return f"Unknown timezone: {timezone}"

    return now.strftime(date_format)