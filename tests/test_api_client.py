from __future__ import annotations

import httpx2

from tests.data.test_defaults import DEFAULT_TASK_RESPONSE, DEFAULT_TOKEN
from todoist_api_python.api import TodoistAPI


def test_supplied_client_is_used() -> None:
    def handle_request(request: httpx2.Request) -> httpx2.Response:
        return httpx2.Response(200, json=DEFAULT_TASK_RESPONSE, request=request)

    client = httpx2.Client(transport=httpx2.MockTransport(handle_request))

    with TodoistAPI(DEFAULT_TOKEN, client=client) as api:
        task = api.get_task(DEFAULT_TASK_RESPONSE["id"])

    assert task.id == DEFAULT_TASK_RESPONSE["id"]
    assert client.is_closed
