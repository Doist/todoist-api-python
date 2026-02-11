from __future__ import annotations

import sys
import uuid
from datetime import date, datetime, timezone

if sys.version_info >= (3, 11):
    from datetime import UTC
else:
    UTC = timezone.utc


def format_date(d: date) -> str:
    """Format a date object as YYYY-MM-DD."""
    return d.isoformat()


def format_datetime(dt: datetime) -> str:
    """
    Format a datetime object.

    YYYY-MM-DDTHH:MM:SS for naive datetimes; YYYY-MM-DDTHH:MM:SSZ for aware datetimes.
    """
    if dt.tzinfo is None:
        return dt.isoformat()
    return dt.astimezone(UTC).isoformat().replace("+00:00", "Z")


def parse_date(date_str: str) -> date:
    """Parse a YYYY-MM-DD string into a date object."""
    return date.fromisoformat(date_str)


def parse_datetime(datetime_str: str) -> datetime:
    """
    Parse a string into a datetime object.

    YYYY-MM-DDTHH:MM:SS for naive datetimes; YYYY-MM-DDTHH:MM:SSZ for aware datetimes.
    """
    if datetime_str.endswith("Z"):
        datetime_str = datetime_str[:-1] + "+00:00"
        return datetime.fromisoformat(datetime_str)
    return datetime.fromisoformat(datetime_str)


def default_request_id_fn() -> str:
    """Generate random UUIDv4s as the default request ID."""
    return str(uuid.uuid4())
