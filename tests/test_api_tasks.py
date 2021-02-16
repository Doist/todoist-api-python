import json
import typing
import urllib
from typing import Any, Dict, List

import pytest
import responses

from tests.data.test_defaults import (
    DEFAULT_REQUEST_ID,
    INVALID_ENTITY_ID,
    REST_API_BASE_URL,
    SYNC_API_BASE_URL,
)
from tests.utils.test_utils import (
    assert_auth_header,
    assert_id_validation,
    assert_request_id_header,
)
from todoist_api_python.api import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import QuickAddResult, Task


@pytest.mark.asyncio
async def test_get_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_task_response: Dict[str, Any],
    default_task: Task,
):
    task_id = 1234
    expected_endpoint = f"{REST_API_BASE_URL}/tasks/{task_id}"

    requests_mock.add(
        responses.GET,
        expected_endpoint,
        json=default_task_response,
        status=200,
    )

    task = todoist_api.get_task(task_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert task == default_task

    task = await todoist_api_async.get_task(task_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert task == default_task


@typing.no_type_check
def test_get_task_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(lambda: todoist_api.get_task(INVALID_ENTITY_ID), requests_mock)


@pytest.mark.asyncio
async def test_get_tasks_minimal(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_tasks_response: List[Dict[str, Any]],
    default_tasks_list: List[Task],
):
    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}/tasks",
        json=default_tasks_response,
        status=200,
    )

    tasks = todoist_api.get_tasks()

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert tasks == default_tasks_list

    tasks = await todoist_api_async.get_tasks()

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert tasks == default_tasks_list


@pytest.mark.asyncio
async def test_get_tasks_full(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_tasks_response: List[Dict[str, Any]],
    default_tasks_list: List[Task],
):
    project_id = 1234
    label_id = 2345
    filter = "today"
    lang = "en"
    ids = [1, 2, 3, 4]

    encoded_ids = urllib.parse.quote(",".join(str(x) for x in ids))
    expected_endpoint = (
        f"{REST_API_BASE_URL}/tasks"
        f"?project_id={project_id}&label_id={label_id}"
        f"&filter={filter}&lang={lang}&ids={encoded_ids}"
    )

    requests_mock.add(
        responses.GET, expected_endpoint, json=default_tasks_response, status=200
    )

    tasks = todoist_api.get_tasks(
        project_id=project_id, label_id=label_id, filter=filter, lang=lang, ids=ids
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert tasks == default_tasks_list

    tasks = await todoist_api_async.get_tasks(
        project_id=project_id, label_id=label_id, filter=filter, lang=lang, ids=ids
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert tasks == default_tasks_list


@pytest.mark.asyncio
async def test_add_task_minimal(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_task_response: Dict[str, Any],
    default_task: Task,
):
    task_content = "Some content"
    expected_payload = {"content": task_content}

    requests_mock.add(
        responses.POST,
        f"{REST_API_BASE_URL}/tasks",
        json=default_task_response,
        status=200,
    )

    new_task = todoist_api.add_task(content=task_content, request_id=DEFAULT_REQUEST_ID)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(expected_payload)
    assert new_task == default_task

    new_task = await todoist_api_async.add_task(
        content=task_content, request_id=DEFAULT_REQUEST_ID
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(expected_payload)
    assert new_task == default_task


@pytest.mark.asyncio
async def test_add_task_full(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_task_response: Dict[str, Any],
    default_task: Task,
):
    task_content = "Some content"

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

    expected_payload: Dict[str, Any] = {"content": task_content}
    expected_payload.update(optional_args)

    requests_mock.add(
        responses.POST,
        f"{REST_API_BASE_URL}/tasks",
        json=default_task_response,
        status=200,
    )

    new_task = todoist_api.add_task(
        content=task_content, request_id=DEFAULT_REQUEST_ID, **optional_args
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(expected_payload)
    assert new_task == default_task

    new_task = await todoist_api_async.add_task(
        content=task_content, request_id=DEFAULT_REQUEST_ID, **optional_args
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(expected_payload)
    assert new_task == default_task


@pytest.mark.asyncio
async def test_update_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
):
    task_id = 123

    args = {
        "content": "Some updated content",
        "label_ids": [123, 456],
        "priority": 4,
        "due_string": "today",
        "due_date": "2021-01-01",
        "due_datetime": "2021-01-01T11:00:00Z",
        "due_lang": "ja",
        "assignee": 321,
    }

    requests_mock.add(
        responses.POST, f"{REST_API_BASE_URL}/tasks/{task_id}", status=204
    )

    response = todoist_api.update_task(
        task_id=task_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(args)
    assert response is True

    response = await todoist_api_async.update_task(
        task_id=task_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(args)
    assert response is True


@typing.no_type_check
def test_update_task_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.update_task(INVALID_ENTITY_ID),
        requests_mock,
    )


@pytest.mark.asyncio
async def test_close_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
):
    task_id = 1234
    expected_endpoint = f"{REST_API_BASE_URL}/tasks/{task_id}/close"

    requests_mock.add(
        responses.POST,
        expected_endpoint,
        status=204,
    )

    response = todoist_api.close_task(task_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert response is True

    response = await todoist_api_async.close_task(task_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert response is True


@typing.no_type_check
def test_close_task_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.close_task(INVALID_ENTITY_ID), requests_mock
    )


@pytest.mark.asyncio
async def test_reopen_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
):
    task_id = 1234
    expected_endpoint = f"{REST_API_BASE_URL}/tasks/{task_id}/reopen"

    requests_mock.add(
        responses.POST,
        expected_endpoint,
        status=204,
    )

    response = todoist_api.reopen_task(task_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert response is True

    response = await todoist_api_async.reopen_task(task_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert response is True


@typing.no_type_check
def test_reopen_task_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.reopen_task(INVALID_ENTITY_ID),
        requests_mock,
    )


@pytest.mark.asyncio
async def test_delete_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
):
    task_id = 1234
    expected_endpoint = f"{REST_API_BASE_URL}/tasks/{task_id}"

    requests_mock.add(
        responses.DELETE,
        expected_endpoint,
        status=204,
    )

    response = todoist_api.delete_task(task_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert response is True

    response = await todoist_api_async.delete_task(task_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert response is True


@typing.no_type_check
def test_delete_task_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.delete_task(INVALID_ENTITY_ID),
        requests_mock,
    )


@pytest.mark.asyncio
async def test_quick_add_task(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_quick_add_response: Dict[str, Any],
    default_quick_add_result: QuickAddResult,
):
    text = "some task"
    expected_payload = {"text": text, "meta": True, "auto_reminder": True}

    requests_mock.add(
        responses.POST,
        f"{SYNC_API_BASE_URL}/quick/add",
        json=default_quick_add_response,
        status=200,
    )

    response = todoist_api.quick_add_task(text=text)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(expected_payload)
    assert response == default_quick_add_result

    response = await todoist_api_async.quick_add_task(text=text)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(expected_payload)
    assert response == default_quick_add_result
