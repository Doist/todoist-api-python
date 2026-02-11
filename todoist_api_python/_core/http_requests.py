from __future__ import annotations

from typing import Any, TypeVar, cast

import httpx

from todoist_api_python._core.http_headers import create_headers

# Timeouts for requests.
#
# 10 seconds for connecting is a recurring default and adheres to common HTTP
# client recommendations of picking a value slightly larger than a multiple of 3.
#
# 60 seconds for reading aligns with Todoist's own internal timeout. All requests
# are forcefully terminated after this time, so there is no point waiting longer.
TIMEOUT = httpx.Timeout(connect=10.0, read=60.0, write=60.0, pool=10.0)

T = TypeVar("T")


def _parse_response(
    response: httpx.Response,
    _result_type: type[T] | None = None,
) -> T:
    response.raise_for_status()

    if response.status_code == httpx.codes.NO_CONTENT:
        return cast("T", response.is_success)

    return cast("T", response.json())


def get(
    client: httpx.Client,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    params: dict[str, Any] | None = None,
    result_type: type[T] | None = None,
) -> T:
    headers = create_headers(token=token, request_id=request_id)

    response = client.get(
        url,
        params=params,
        headers=headers,
        timeout=TIMEOUT,
    )

    return _parse_response(response, result_type)


async def get_async(
    client: httpx.AsyncClient,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    params: dict[str, Any] | None = None,
    result_type: type[T] | None = None,
) -> T:
    headers = create_headers(token=token, request_id=request_id)

    response = await client.get(
        url,
        params=params,
        headers=headers,
        timeout=TIMEOUT,
    )

    return _parse_response(response, result_type)


def post(
    client: httpx.Client,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    *,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    result_type: type[T] | None = None,
) -> T:
    headers = create_headers(token=token, request_id=request_id)

    response = client.post(
        url,
        headers=headers,
        json=data if data else None,
        params=params,
        timeout=TIMEOUT,
    )

    return _parse_response(response, result_type)


async def post_async(
    client: httpx.AsyncClient,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    *,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
    result_type: type[T] | None = None,
) -> T:
    headers = create_headers(token=token, request_id=request_id)

    response = await client.post(
        url,
        headers=headers,
        json=data if data else None,
        params=params,
        timeout=TIMEOUT,
    )

    return _parse_response(response, result_type)


def delete(
    client: httpx.Client,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    params: dict[str, Any] | None = None,
) -> bool:
    headers = create_headers(token=token, request_id=request_id)

    response = client.delete(url, params=params, headers=headers, timeout=TIMEOUT)

    response.raise_for_status()
    return response.is_success


async def delete_async(
    client: httpx.AsyncClient,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    params: dict[str, Any] | None = None,
) -> bool:
    headers = create_headers(token=token, request_id=request_id)

    response = await client.delete(url, params=params, headers=headers, timeout=TIMEOUT)

    response.raise_for_status()
    return response.is_success
