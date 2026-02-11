from __future__ import annotations

import sys
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Any

if sys.version_info >= (3, 11):
    from datetime import UTC
else:
    UTC = timezone.utc

import pytest

from tests.data.test_defaults import DEFAULT_API_URL, PaginatedResults
from tests.utils.test_utils import (
    auth_matcher,
    data_matcher,
    enumerate_async,
    param_matcher,
    request_id_matcher,
)

if TYPE_CHECKING:
    from tests.utils.http_mock import RequestsMock
    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Task


@pytest.mark.asyncio
async def test_get_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_task_response: dict[str, Any],
    default_task: Task,
) -> None:
    task_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/tasks/{task_id}"

    requests_mock.add(
        method="GET",
        url=endpoint,
        json=default_task_response,
        match=[auth_matcher(), request_id_matcher()],
    )

    task = todoist_api.get_task(task_id)

    assert len(requests_mock.calls) == 1
    assert task == default_task

    task = await todoist_api_async.get_task(task_id)

    assert len(requests_mock.calls) == 2
    assert task == default_task


@pytest.mark.asyncio
async def test_get_tasks(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_tasks_response: list[PaginatedResults],
    default_tasks_list: list[list[Task]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/tasks"

    cursor: str | None = None
    for page in default_tasks_response:
        requests_mock.add(
            method="GET",
            url=endpoint,
            json=page,
            status=200,
            match=[auth_matcher(), request_id_matcher(), param_matcher({}, cursor)],
        )
        cursor = page["next_cursor"]

    count = 0

    tasks_iter = todoist_api.get_tasks()

    for i, tasks in enumerate(tasks_iter):
        assert len(requests_mock.calls) == count + 1
        assert tasks == default_tasks_list[i]
        count += 1

    tasks_async_iter = await todoist_api_async.get_tasks()

    async for i, tasks in enumerate_async(tasks_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert tasks == default_tasks_list[i]
        count += 1


@pytest.mark.asyncio
async def test_get_tasks_with_filters(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_tasks_response: list[PaginatedResults],
    default_tasks_list: list[list[Task]],
) -> None:
    project_id = "123"
    section_id = "456"
    parent_id = "789"
    label = "test-label"
    ids = ["1", "2", "3"]
    limit = 30

    params: dict[str, Any] = {
        "project_id": project_id,
        "section_id": section_id,
        "parent_id": parent_id,
        "label": label,
        "ids": ",".join(ids),
        "limit": limit,
    }

    endpoint = f"{DEFAULT_API_URL}/tasks"

    cursor: str | None = None
    for page in default_tasks_response:
        requests_mock.add(
            method="GET",
            url=endpoint,
            json=page,
            status=200,
            match=[auth_matcher(), request_id_matcher(), param_matcher(params, cursor)],
        )
        cursor = page["next_cursor"]

    count = 0

    tasks_iter = todoist_api.get_tasks(
        project_id=project_id,
        section_id=section_id,
        parent_id=parent_id,
        label=label,
        ids=ids,
        limit=limit,
    )

    for i, tasks in enumerate(tasks_iter):
        assert len(requests_mock.calls) == count + 1
        assert tasks == default_tasks_list[i]
        count += 1

    tasks_async_iter = await todoist_api_async.get_tasks(
        project_id=project_id,
        section_id=section_id,
        parent_id=parent_id,
        label=label,
        ids=ids,
        limit=limit,
    )

    async for i, tasks in enumerate_async(tasks_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert tasks == default_tasks_list[i]
        count += 1


@pytest.mark.asyncio
async def test_filter_tasks(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_tasks_response: list[PaginatedResults],
    default_tasks_list: list[list[Task]],
) -> None:
    query = "today or overdue"
    lang = "en"
    params = {
        "query": "today or overdue",
        "lang": "en",
    }

    endpoint = f"{DEFAULT_API_URL}/tasks/filter"

    cursor: str | None = None
    for page in default_tasks_response:
        requests_mock.add(
            method="GET",
            url=endpoint,
            json=page,
            status=200,
            match=[auth_matcher(), request_id_matcher(), param_matcher(params, cursor)],
        )
        cursor = page["next_cursor"]

    count = 0

    tasks_iter = todoist_api.filter_tasks(
        query=query,
        lang=lang,
    )

    for i, tasks in enumerate(tasks_iter):
        assert len(requests_mock.calls) == count + 1
        assert tasks == default_tasks_list[i]
        count += 1

    # Test async iterator
    tasks_async_iter = await todoist_api_async.filter_tasks(
        query=query,
        lang=lang,
    )

    async for i, tasks in enumerate_async(tasks_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert tasks == default_tasks_list[i]
        count += 1


@pytest.mark.asyncio
async def test_add_task_minimal(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_task_response: dict[str, Any],
    default_task: Task,
) -> None:
    content = "Some content"

    requests_mock.add(
        method="POST",
        url=f"{DEFAULT_API_URL}/tasks",
        json=default_task_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher({"content": content}),
        ],
    )

    new_task = todoist_api.add_task(content=content)

    assert len(requests_mock.calls) == 1
    assert new_task == default_task

    new_task = await todoist_api_async.add_task(content=content)

    assert len(requests_mock.calls) == 2
    assert new_task == default_task


@pytest.mark.asyncio
async def test_add_task_full(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_task_response: dict[str, Any],
    default_task: Task,
) -> None:
    content = "Some content"
    due_datetime = datetime(2021, 1, 1, 11, 0, 0, tzinfo=UTC)
    args: dict[str, Any] = {
        "description": "A description",
        "project_id": "123",
        "section_id": "456",
        "parent_id": "789",
        "labels": ["label1", "label2"],
        "priority": 4,
        "due_string": "today",
        "due_lang": "en",
        "assignee_id": "321",
        "order": 3,
        "auto_reminder": True,
        "auto_parse_labels": True,
        "duration": 60,
        "duration_unit": "minute",
    }

    requests_mock.add(
        method="POST",
        url=f"{DEFAULT_API_URL}/tasks",
        json=default_task_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher(
                {
                    "content": content,
                    "due_datetime": due_datetime.strftime("%Y-%m-%dT%H:%M:%SZ"),
                }
                | args
            ),
        ],
    )

    new_task = todoist_api.add_task(content=content, due_datetime=due_datetime, **args)

    assert len(requests_mock.calls) == 1
    assert new_task == default_task

    new_task = await todoist_api_async.add_task(
        content=content, due_datetime=due_datetime, **args
    )

    assert len(requests_mock.calls) == 2
    assert new_task == default_task


@pytest.mark.asyncio
async def test_add_task_quick(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_task_meta_response: dict[str, Any],
    default_task_meta: Task,
) -> None:
    text = "Buy milk tomorrow at 9am #Shopping @errands"
    note = "Whole milk x6"
    auto_reminder = True

    requests_mock.add(
        method="POST",
        url=f"{DEFAULT_API_URL}/tasks/quick",
        json=default_task_meta_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher(
                {
                    "meta": True,
                    "text": text,
                    "auto_reminder": auto_reminder,
                    "note": note,
                }
            ),
        ],
    )

    task = todoist_api.add_task_quick(
        text=text,
        note=note,
        auto_reminder=auto_reminder,
    )

    assert len(requests_mock.calls) == 1
    assert task == default_task_meta

    task = await todoist_api_async.add_task_quick(
        text=text,
        note=note,
        auto_reminder=auto_reminder,
    )

    assert len(requests_mock.calls) == 2
    assert task == default_task_meta


@pytest.mark.asyncio
async def test_update_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_task: Task,
) -> None:
    args: dict[str, Any] = {
        "content": "Updated content",
        "description": "Updated description",
        "labels": ["label1", "label2"],
        "priority": 2,
    }
    updated_task_dict = default_task.to_dict() | args

    requests_mock.add(
        method="POST",
        url=f"{DEFAULT_API_URL}/tasks/{default_task.id}",
        json=updated_task_dict,
        status=200,
        match=[auth_matcher(), request_id_matcher(), data_matcher(args)],
    )

    response = todoist_api.update_task(task_id=default_task.id, **args)

    assert len(requests_mock.calls) == 1
    assert response == Task.from_dict(updated_task_dict)

    response = await todoist_api_async.update_task(task_id=default_task.id, **args)

    assert len(requests_mock.calls) == 2
    assert response == Task.from_dict(updated_task_dict)


@pytest.mark.asyncio
async def test_complete_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
) -> None:
    task_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/tasks/{task_id}/close"

    requests_mock.add(
        method="POST",
        url=endpoint,
        status=204,
        match=[auth_matcher(), request_id_matcher()],
    )

    response = todoist_api.complete_task(task_id)

    assert len(requests_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.complete_task(task_id)

    assert len(requests_mock.calls) == 2
    assert response is True


@pytest.mark.asyncio
async def test_uncomplete_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
) -> None:
    task_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/tasks/{task_id}/reopen"

    requests_mock.add(
        method="POST",
        url=endpoint,
        status=204,
        match=[auth_matcher(), request_id_matcher()],
    )

    response = todoist_api.uncomplete_task(task_id)

    assert len(requests_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.uncomplete_task(task_id)

    assert len(requests_mock.calls) == 2
    assert response is True


@pytest.mark.asyncio
async def test_move_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
) -> None:
    task_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/tasks/{task_id}/move"

    requests_mock.add(
        method="POST",
        url=endpoint,
        status=204,
        match=[auth_matcher(), request_id_matcher()],
    )

    response = todoist_api.move_task(task_id, project_id="123")

    assert len(requests_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.move_task(task_id, section_id="456")

    assert len(requests_mock.calls) == 2
    assert response is True

    response = await todoist_api_async.move_task(task_id, parent_id="789")

    assert len(requests_mock.calls) == 3
    assert response is True

    with pytest.raises(
        ValueError,
        match="Either `project_id`, `section_id`, or `parent_id` must be provided.",
    ):
        response = await todoist_api_async.move_task(task_id)


@pytest.mark.asyncio
async def test_delete_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
) -> None:
    task_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/tasks/{task_id}"

    requests_mock.add(
        method="DELETE",
        url=endpoint,
        status=204,
        match=[auth_matcher(), request_id_matcher()],
    )

    response = todoist_api.delete_task(task_id)

    assert len(requests_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.delete_task(task_id)

    assert len(requests_mock.calls) == 2
    assert response is True
