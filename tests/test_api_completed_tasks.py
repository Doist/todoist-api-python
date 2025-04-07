from __future__ import annotations

from datetime import UTC, datetime
from typing import TYPE_CHECKING, Any

import pytest
import responses

from tests.data.test_defaults import DEFAULT_API_URL, PaginatedItems
from tests.utils.test_utils import auth_matcher, enumerate_async, param_matcher
from todoist_api_python._core.utils import format_datetime

if TYPE_CHECKING:
    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync
    from todoist_api_python.models import Task


@pytest.mark.asyncio
async def test_get_completed_tasks_by_due_date(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_completed_tasks_response: list[PaginatedItems],
    default_completed_tasks_list: list[list[Task]],
) -> None:
    since = datetime(2024, 1, 1, 0, 0, 0, tzinfo=UTC)
    until = datetime(2024, 2, 1, 0, 0, 0, tzinfo=UTC)
    project_id = "6X7rM8997g3RQmvh"
    filter_query = "p1"

    params = {
        "since": format_datetime(since),
        "until": format_datetime(until),
        "project_id": project_id,
        "filter_query": filter_query,
    }

    endpoint = f"{DEFAULT_API_URL}/tasks/completed/by_due_date"

    cursor: str | None = None
    for page in default_completed_tasks_response:
        requests_mock.add(
            method=responses.GET,
            url=endpoint,
            json=page,
            status=200,
            match=[auth_matcher(), param_matcher(params, cursor)],
        )
        cursor = page["next_cursor"]

    count = 0

    tasks_iter = todoist_api.get_completed_tasks_by_due_date(
        since=since,
        until=until,
        project_id=project_id,
        filter_query=filter_query,
    )

    for i, tasks in enumerate(tasks_iter):
        assert len(requests_mock.calls) == count + 1
        assert tasks == default_completed_tasks_list[i]
        count += 1

    tasks_async_iter = await todoist_api_async.get_completed_tasks_by_due_date(
        since=since,
        until=until,
        project_id=project_id,
        filter_query=filter_query,
    )

    async for i, tasks in enumerate_async(tasks_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert tasks == default_completed_tasks_list[i]
        count += 1


@pytest.mark.asyncio
async def test_get_completed_tasks_by_completion_date(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_completed_tasks_response: list[PaginatedItems],
    default_completed_tasks_list: list[list[Task]],
) -> None:
    since = datetime(2024, 3, 1, 0, 0, 0)  # noqa: DTZ001
    until = datetime(2024, 4, 1, 0, 0, 0)  # noqa: DTZ001
    workspace_id = "123"
    filter_query = "@label"

    params: dict[str, Any] = {
        "since": format_datetime(since),
        "until": format_datetime(until),
        "workspace_id": workspace_id,
        "filter_query": filter_query,
    }

    endpoint = f"{DEFAULT_API_URL}/tasks/completed/by_completion_date"

    cursor: str | None = None
    for page in default_completed_tasks_response:
        requests_mock.add(
            method=responses.GET,
            url=endpoint,
            json=page,
            status=200,
            match=[auth_matcher(), param_matcher(params, cursor)],
        )
        cursor = page["next_cursor"]

    count = 0

    tasks_iter = todoist_api.get_completed_tasks_by_completion_date(
        since=since,
        until=until,
        workspace_id=workspace_id,
        filter_query=filter_query,
    )

    for i, tasks in enumerate(tasks_iter):
        assert len(requests_mock.calls) == count + 1
        assert tasks == default_completed_tasks_list[i]
        count += 1

    tasks_async_iter = await todoist_api_async.get_completed_tasks_by_completion_date(
        since=since,
        until=until,
        workspace_id=workspace_id,
        filter_query=filter_query,
    )

    async for i, tasks in enumerate_async(tasks_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert tasks == default_completed_tasks_list[i]
        count += 1
