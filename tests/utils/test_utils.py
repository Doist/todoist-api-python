from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, TypeVar

from responses import matchers

from tests.data.test_defaults import (
    DEFAULT_TOKEN,
)
from todoist_api_python.api import TodoistAPI

if TYPE_CHECKING:
    from collections.abc import AsyncIterable, AsyncIterator, Callable


MATCH_ANY_REGEX = re.compile(".*")


def auth_matcher() -> Callable[..., Any]:
    return matchers.header_matcher({"Authorization": f"Bearer {DEFAULT_TOKEN}"})


def param_matcher(
    params: dict[str, str], cursor: str | None = None
) -> Callable[..., Any]:
    return matchers.query_param_matcher(params | ({"cursor": cursor} if cursor else {}))


def data_matcher(data: dict[str, Any]) -> Callable[..., Any]:
    return matchers.json_params_matcher(data)


def get_todoist_api_patch(method: Callable[..., Any] | None) -> str:
    module = TodoistAPI.__module__
    name = TodoistAPI.__qualname__

    return f"{module}.{name}.{method.__name__}" if method else f"{module}.{name}"


T = TypeVar("T")


async def enumerate_async(
    iterable: AsyncIterable[T], start: int = 0
) -> AsyncIterator[tuple[int, T]]:
    index = start
    async for value in iterable:
        yield index, value
        index += 1
