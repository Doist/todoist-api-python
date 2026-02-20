from __future__ import annotations

from typing import Any

import httpx

from todoist_api_python._core.http_headers import create_headers

# Timeouts for requests.
#
# 10 seconds for connecting is a recurring default and adheres to python-requests's
# recommendation of picking a value slightly larger than a multiple of 3.
#
# 60 seconds for reading aligns with Todoist's own internal timeout. All requests
# are forcefully terminated after this time, so there is no point waiting longer.
TIMEOUT = httpx.Timeout(connect=10.0, read=60.0, write=60.0, pool=10.0)


def get(
    client: httpx.Client,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    params: dict[str, Any] | None = None,
) -> httpx.Response:
    headers = create_headers(token=token, request_id=request_id)

    response = client.get(
        url,
        params=params,
        headers=headers,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response


async def get_async(
    client: httpx.AsyncClient,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    params: dict[str, Any] | None = None,
) -> httpx.Response:
    headers = create_headers(token=token, request_id=request_id)

    response = await client.get(
        url,
        params=params,
        headers=headers,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response


def post(
    client: httpx.Client,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    *,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
) -> httpx.Response:
    headers = create_headers(token=token, request_id=request_id)

    response = client.post(
        url,
        headers=headers,
        json=data,
        params=params,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response


async def post_async(
    client: httpx.AsyncClient,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    *,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
) -> httpx.Response:
    headers = create_headers(token=token, request_id=request_id)

    response = await client.post(
        url,
        headers=headers,
        json=data,
        params=params,
        timeout=TIMEOUT,
    )
    response.raise_for_status()
    return response


def delete(
    client: httpx.Client,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    params: dict[str, Any] | None = None,
) -> httpx.Response:
    headers = create_headers(token=token, request_id=request_id)

    response = client.delete(url, params=params, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return response


async def delete_async(
    client: httpx.AsyncClient,
    url: str,
    token: str | None = None,
    request_id: str | None = None,
    params: dict[str, Any] | None = None,
) -> httpx.Response:
    headers = create_headers(token=token, request_id=request_id)

    response = await client.delete(url, params=params, headers=headers, timeout=TIMEOUT)
    response.raise_for_status()
    return response


def response_json_dict(response: httpx.Response) -> dict[str, Any]:
    data = response.json()
    if not isinstance(data, dict):
        raise TypeError(
            f"Expected response to be a JSON object, got {type(data).__name__}."
        )
    return data
