from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import parse_qs, urlparse

import pytest
import responses

from tests.data.test_defaults import SYNC_API_BASE_URL
from tests.utils.test_utils import assert_auth_header
from todoist_api_python.endpoints import COMPLETED_ITEMS_ENDPOINT

if TYPE_CHECKING:
    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync
    from todoist_api_python.models import CompletedItems


@pytest.mark.asyncio
async def test_get_completed_items(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_completed_items_response: dict[str, Any],
    default_completed_items: CompletedItems,
) -> None:
    project_id = "1234"
    section_id = "5678"
    item_id = "90ab"
    last_seen_id = "cdef"
    limit = 30
    cursor = "ghij"

    def assert_query(url: str) -> None:
        queries = parse_qs(urlparse(url).query)
        assert queries.get("project_id") == [project_id]
        assert queries.get("section_id") == [section_id]
        assert queries.get("item_id") == [item_id]
        assert queries.get("last_seen_id") == [last_seen_id]
        assert queries.get("limit") == [str(limit)]
        assert queries.get("cursor") == [cursor]

    expected_endpoint = f"{SYNC_API_BASE_URL}/{COMPLETED_ITEMS_ENDPOINT}"

    requests_mock.add(
        responses.GET,
        expected_endpoint,
        json=default_completed_items_response,
        status=200,
    )

    completed_items = todoist_api.get_completed_items(
        project_id, section_id, item_id, last_seen_id, limit, cursor
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_query(requests_mock.calls[0].request.url)
    assert completed_items == default_completed_items

    completed_items = await todoist_api_async.get_completed_items(
        project_id, section_id, item_id, last_seen_id, limit, cursor
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_query(requests_mock.calls[1].request.url)
    assert completed_items == default_completed_items
