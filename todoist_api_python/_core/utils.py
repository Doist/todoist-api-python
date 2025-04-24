from __future__ import annotations

import asyncio
import sys
from datetime import date, datetime, timezone
from typing import TYPE_CHECKING, TypeVar, cast

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator, Callable, Iterator

if sys.version_info >= (3, 11):
    from datetime import UTC
else:
    UTC = timezone.utc

T = TypeVar("T")


async def run_async(func: Callable[[], T]) -> T:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func)


async def generate_async(iterator: Iterator[T]) -> AsyncGenerator[T]:
    def get_next_item() -> tuple[bool, T | None]:
        try:
            return True, next(iterator)
        except StopIteration:
            return False, None

    while True:
        has_more, item = await run_async(get_next_item)
        if has_more is True:
            yield cast("T", item)
        else:
            break


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
    from datetime import datetime

    if datetime_str.endswith("Z"):
        datetime_str = datetime_str[:-1] + "+00:00"
        return datetime.fromisoformat(datetime_str)
    return datetime.fromisoformat(datetime_str)
