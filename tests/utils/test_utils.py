from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any, TypeVar

from tests.data.test_defaults import (
    DEFAULT_TOKEN,
)
from todoist_api_python.api import TodoistAPI

if TYPE_CHECKING:
    from collections.abc import AsyncIterable, AsyncIterator, Callable

    import httpx


RE_UUID = re.compile(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$", re.IGNORECASE)


def auth_matcher() -> Callable[[httpx.Request], None]:
    def matcher(request: httpx.Request) -> None:
        assert request.headers.get("Authorization") == f"Bearer {DEFAULT_TOKEN}"

    return matcher


def request_id_matcher(
    request_id: str | None = None,
) -> Callable[[httpx.Request], None]:
    def matcher(request: httpx.Request) -> None:
        value = request.headers.get("X-Request-Id")
        assert value is not None
        if request_id is not None:
            assert value == request_id
        else:
            assert RE_UUID.match(value) is not None

    return matcher


def _normalize_param_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)


def param_matcher(
    params: dict[str, Any], cursor: str | None = None
) -> Callable[[httpx.Request], None]:
    expected = params | ({"cursor": cursor} if cursor else {})
    normalized_expected = {
        key: _normalize_param_value(value) for key, value in expected.items()
    }

    def matcher(request: httpx.Request) -> None:
        normalized_actual = dict(request.url.params.multi_items())
        assert normalized_actual == normalized_expected

    return matcher


def data_matcher(data: dict[str, Any]) -> Callable[[httpx.Request], None]:
    def matcher(request: httpx.Request) -> None:
        assert request.content
        actual = json.loads(request.content.decode())
        assert actual == data

    return matcher


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
