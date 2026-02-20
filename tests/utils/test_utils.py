from __future__ import annotations

from typing import TYPE_CHECKING, Any, TypeVar, Union, cast

from tests.data.test_defaults import DEFAULT_REQUEST_ID, DEFAULT_TOKEN

if TYPE_CHECKING:
    from collections.abc import AsyncIterable, AsyncIterator

    import respx

_UNSET = object()

JSONValue = Union[dict[str, object], list[object], str, int, float, bool, None]


def auth_headers(token: str = DEFAULT_TOKEN) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def request_id_headers(request_id: str = DEFAULT_REQUEST_ID) -> dict[str, str]:
    return {"X-Request-Id": request_id}


def api_headers(
    token: str = DEFAULT_TOKEN,
    request_id: str = DEFAULT_REQUEST_ID,
) -> dict[str, str]:
    return auth_headers(token) | request_id_headers(request_id)


def mock_route(
    router: respx.MockRouter,
    method: str,
    url: str,
    *,
    response_status: int = 200,
    response_json: JSONValue | object = _UNSET,
    request_params: dict[str, Any] | None = None,
    request_headers: dict[str, str] | None = None,
    request_json: JSONValue | object = _UNSET,
) -> None:
    """Register a route with declarative request lookups and mocked response data."""
    route_lookups: dict[str, Any] = {"method": method, "url": url}

    if request_params is not None:
        route_lookups["params__eq"] = _normalize_params(request_params) or {}
    if request_headers is not None:
        route_lookups["headers__contains"] = request_headers
    if request_json is not _UNSET:
        route_lookups["json__eq"] = cast("JSONValue", request_json)

    route = router.route(**route_lookups)

    if response_json is _UNSET:
        route.respond(status_code=response_status)
    else:
        route.respond(status_code=response_status, json=cast("Any", response_json))


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
