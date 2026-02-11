from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

import httpx

from tests.data.test_defaults import (
    DEFAULT_TOKEN,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterable, AsyncIterator, Callable

    import respx

RE_UUID = re.compile(r"^[\da-f]{8}-([\da-f]{4}-){3}[\da-f]{12}$", re.IGNORECASE)
_UNSET = object()

JSONValue = Union[dict[str, object], list[object], str, int, float, bool, None]


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


def data_matcher(data: dict[str, Any]) -> Callable[[httpx.Request], None]:
    def matcher(request: httpx.Request) -> None:
        assert request.content
        actual = json.loads(request.content.decode())
        assert actual == data

    return matcher


def mock_route(
    router: respx.MockRouter,
    method: str,
    url: str,
    *,
    status: int = 200,
    json: JSONValue | object = _UNSET,
    params: dict[str, Any] | None = None,
    matchers: list[Callable[[httpx.Request], None]] | None = None,
) -> None:
    """Register a route with optional runtime request assertions.

    Query params use `params__eq` so routes with the same method/path are still
    matched deterministically by their exact query string values.
    """
    normalized_params = _normalize_params(params)
    runtime_matchers = matchers or []

    def handler(request: httpx.Request) -> httpx.Response:
        for matcher in runtime_matchers:
            matcher(request)

        if json is _UNSET:
            return httpx.Response(status_code=status, request=request)

        return httpx.Response(
            status_code=status,
            json=cast("JSONValue", json),
            request=request,
        )

    if normalized_params is None:
        route = router.route(method=method, url=url)
    else:
        route = router.route(method=method, url=url, params__eq=normalized_params)

    route.mock(side_effect=handler)


T = TypeVar("T")


async def enumerate_async(
    iterable: AsyncIterable[T], start: int = 0
) -> AsyncIterator[tuple[int, T]]:
    index = start
    async for value in iterable:
        yield index, value
        index += 1


def _normalize_params(params: dict[str, Any] | None) -> dict[str, str] | None:
    if params is None:
        return None

    return {key: _normalize_param_value(value) for key, value in params.items()}


def _normalize_param_value(value: object) -> str:
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value)
