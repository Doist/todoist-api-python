from typing import Callable, List, Optional
from unittest.mock import MagicMock, patch

import pytest

from tests.data.test_defaults import DEFAULT_TOKEN
from todoist_api_python import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Task


def _get_todoist_api_patch(method: Optional[Callable]) -> str:
    module = TodoistAPI.__module__
    name = TodoistAPI.__qualname__

    return f"{module}.{name}.{method.__name__}" if method else f"{module}.{name}"


@patch(_get_todoist_api_patch(TodoistAPI.__init__))
@pytest.mark.asyncio
async def test_constructs_api_with_token(sync_api_constructor: MagicMock):
    sync_api_constructor.return_value = None
    TodoistAPIAsync(DEFAULT_TOKEN)

    sync_api_constructor.assert_called_once_with(DEFAULT_TOKEN)


@patch(_get_todoist_api_patch(TodoistAPI.get_task))
@pytest.mark.asyncio
async def test_get_task(
    get_task: MagicMock, todoist_api_async: TodoistAPIAsync, default_task: Task
):
    task_id = 123
    get_task.return_value = default_task

    task = await todoist_api_async.get_task(task_id)

    get_task.assert_called_once_with(task_id)
    assert task == default_task


@patch(_get_todoist_api_patch(TodoistAPI.get_tasks))
@pytest.mark.asyncio
async def test_get_tasks(
    get_tasks: MagicMock,
    todoist_api_async: TodoistAPIAsync,
    default_tasks_list: List[Task],
):
    get_tasks.return_value = default_tasks_list
    args = {
        "project_id": 123,
        "label_id": 456,
        "filter": "today",
        "lang": "en",
        "ids": [123, 456],
    }

    tasks = await todoist_api_async.get_tasks(**args)

    get_tasks.assert_called_once_with(**args)
    assert tasks == default_tasks_list


@patch(_get_todoist_api_patch(TodoistAPI.add_task))
@pytest.mark.asyncio
async def test_add_task(
    add_task: MagicMock,
    todoist_api_async: TodoistAPIAsync,
    default_task: Task,
):
    add_task.return_value = default_task
    task_content = "A task"
    optional_args = {
        "project_id": 123,
        "section_id": 456,
        "parent_id": 789,
        "order": 3,
        "label_ids": [123, 456],
        "priority": 4,
        "due_string": "today",
        "due_date": "2021-01-01",
        "due_datetime": "2021-01-01T11:00:00Z",
        "due_lang": "ja",
        "assignee": 321,
    }

    task = await todoist_api_async.add_task(content=task_content, **optional_args)

    add_task.assert_called_once_with(task_content, **optional_args)
    assert task == default_task


@patch(_get_todoist_api_patch(TodoistAPI.update_task))
@pytest.mark.asyncio
async def test_update_task(
    update_task: MagicMock,
    todoist_api_async: TodoistAPIAsync,
):
    task_id = 123
    update_task.return_value = True
    args = {
        "content": "A task",
        "project_id": 123,
        "section_id": 456,
        "parent_id": 789,
        "order": 3,
        "label_ids": [123, 456],
        "priority": 4,
        "due_string": "today",
        "due_date": "2021-01-01",
        "due_datetime": "2021-01-01T11:00:00Z",
        "due_lang": "ja",
        "assignee": 321,
    }

    result = await todoist_api_async.update_task(task_id, **args)

    update_task.assert_called_once_with(task_id, **args)
    assert result is True


@patch(_get_todoist_api_patch(TodoistAPI.close_task))
@pytest.mark.asyncio
async def test_close_task(close_task: MagicMock, todoist_api_async: TodoistAPIAsync):
    task_id = 123
    close_task.return_value = True

    result = await todoist_api_async.close_task(task_id)

    close_task.assert_called_once_with(task_id)
    assert result is True


@patch(_get_todoist_api_patch(TodoistAPI.reopen_task))
@pytest.mark.asyncio
async def test_reopen_task(reopen_task: MagicMock, todoist_api_async: TodoistAPIAsync):
    task_id = 123
    reopen_task.return_value = True

    result = await todoist_api_async.reopen_task(task_id)

    reopen_task.assert_called_once_with(task_id)
    assert result is True


@patch(_get_todoist_api_patch(TodoistAPI.delete_task))
@pytest.mark.asyncio
async def test_delete_task(delete_task: MagicMock, todoist_api_async: TodoistAPIAsync):
    task_id = 123
    delete_task.return_value = True

    result = await todoist_api_async.delete_task(task_id)

    delete_task.assert_called_once_with(task_id)
    assert result is True
