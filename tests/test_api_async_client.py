from __future__ import annotations

import asyncio
import warnings

import httpx2
import pytest

from tests.data.test_defaults import DEFAULT_TASK_RESPONSE, DEFAULT_TOKEN
from todoist_api_python.api_async import TodoistAPIAsync


@pytest.mark.asyncio
async def test_supplied_async_client_is_used() -> None:
    async def handle_request(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json=DEFAULT_TASK_RESPONSE, request=request)

    client = httpx2.AsyncClient(transport=httpx2.MockTransport(handle_request))

    async with TodoistAPIAsync(DEFAULT_TOKEN, client=client) as api:
        task = await api.get_task(DEFAULT_TASK_RESPONSE["id"])

    assert task.id == DEFAULT_TASK_RESPONSE["id"]
    assert client.is_closed


def test_warns_if_async_client_is_not_closed() -> None:
    api = TodoistAPIAsync(DEFAULT_TOKEN)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ResourceWarning)
        api.__del__()

    assert any(item.category is ResourceWarning for item in caught)

    asyncio.run(api.close())
