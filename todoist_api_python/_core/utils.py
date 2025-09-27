from __future__ import annotations

import asyncio
import sys
import uuid
import inspect
import logging
from functools import wraps
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


def default_request_id_fn() -> str:
    """Generate random UUIDv4s as the default request ID."""
    return str(uuid.uuid4())


def log_calls(func: Callable[..., T]) -> Callable[..., T]:
    """
    Decorator to log calls to a callable. Arguments and returned values are included in the log
    """
    # Create a 'call count' variable to differentiate between multiple calls to the same function
    # Useful for recursion
    func._call_count = 0

    # Use inspect to get the module of the caller and the appropriate logger
    funcs_module = inspect.getmodule(func)
    logger = logging.getLogger(funcs_module.__name__ if funcs_module else "")
    logger.debug(f"Wrapping function {func.__name__} with logger {logger}")

    # Create the wrapped function which logs on function entry, with the arguments
    # and on exit, with the return value
    # Function calls are numbered to make the log file easier to search
    @wraps(func)
    def wrapper(*args, **kwargs):
        func._call_count += 1
        logger.debug(f"Call to function {func.__name__} (#{func._call_count}): Entering with args={args}, kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"Call to function {func.__name__} (#{func._call_count}): Exiting with result={result}")
        return result

    return wrapper


def log_method_calls(exclude_dunder: bool = True) -> Callable[[type], type]:
    """
    Class decorator to log calls to all methods of a class. Arguments and returned values are
    included in the log.

    Args:
        exclude_dunder (bool): If True, exclude dunder methods (methods with names starting and
            ending with '__') from logging. Default is True.
    """
    def class_decorator(cls: type) -> type:
        for attr_name, attr_value in cls.__dict__.items():
            if callable(attr_value):
                if exclude_dunder and attr_name.startswith("__") and attr_name.endswith("__"):
                    continue
                decorated_attr = log_calls(attr_value)
                setattr(cls, attr_name, decorated_attr)
        return cls

    return class_decorator
