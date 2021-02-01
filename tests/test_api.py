import json
import urllib
from typing import Any, Dict, List

import responses

from tests.conftest import DEFAULT_TOKEN
from tests.data.test_defaults import API_BASE_URL, DEFAULT_REQUEST_ID
from todoist_api_python import TodoistAPI
from todoist_api_python.models import Task


def assert_auth_header(request):
    assert request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"


def assert_request_id_header(request):
    assert request.headers["X-Request-Id"] == DEFAULT_REQUEST_ID


@responses.activate
def test_get_task(
    todoist_api: TodoistAPI, default_task_response: Dict[str, Any], default_task: Task
):
    task_id = 1234
    expected_endpoint = f"{API_BASE_URL}/tasks/{task_id}"

    responses.add(
        responses.GET,
        expected_endpoint,
        json=default_task_response,
        status=200,
    )

    task = todoist_api.get_task(task_id)

    assert len(responses.calls) == 1
    assert_auth_header(responses.calls[0].request)
    assert task == default_task


@responses.activate
def test_get_tasks_minimal(
    todoist_api: TodoistAPI,
    default_tasks_response: List[Dict[str, Any]],
    default_tasks_list: List[Task],
):
    responses.add(
        responses.GET, f"{API_BASE_URL}/tasks", json=default_tasks_response, status=200
    )

    tasks = todoist_api.get_tasks()

    assert len(responses.calls) == 1
    assert_auth_header(responses.calls[0].request)
    assert tasks == default_tasks_list


@responses.activate
def test_get_tasks_full(
    todoist_api: TodoistAPI,
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
        f"{API_BASE_URL}/tasks"
        f"?project_id={project_id}&label_id={label_id}"
        f"&filter={filter}&lang={lang}&ids={encoded_ids}"
    )

    responses.add(
        responses.GET, expected_endpoint, json=default_tasks_response, status=200
    )

    tasks = todoist_api.get_tasks(
        project_id=project_id, label_id=label_id, filter=filter, lang=lang, ids=ids
    )

    assert len(responses.calls) == 1
    assert_auth_header(responses.calls[0].request)
    assert tasks == default_tasks_list


@responses.activate
def test_add_task_minimal(
    todoist_api: TodoistAPI,
    default_task_response: Dict[str, Any],
    default_task: Task,
):
    task_content = "Some content"
    expected_payload = {"content": task_content}

    responses.add(
        responses.POST, f"{API_BASE_URL}/tasks", json=default_task_response, status=200
    )

    new_task = todoist_api.add_task(content=task_content, request_id=DEFAULT_REQUEST_ID)

    assert len(responses.calls) == 1
    assert_auth_header(responses.calls[0].request)
    assert_request_id_header(responses.calls[0].request)
    assert responses.calls[0].request.body == json.dumps(expected_payload)
    assert new_task == default_task


@responses.activate
def test_add_task_full(
    todoist_api: TodoistAPI,
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

    responses.add(
        responses.POST, f"{API_BASE_URL}/tasks", json=default_task_response, status=200
    )

    new_task = todoist_api.add_task(
        content=task_content, request_id=DEFAULT_REQUEST_ID, **optional_args
    )

    assert len(responses.calls) == 1
    assert_auth_header(responses.calls[0].request)
    assert_request_id_header(responses.calls[0].request)
    assert responses.calls[0].request.body == json.dumps(expected_payload)
    assert new_task == default_task


@responses.activate
def test_update_task_full(todoist_api: TodoistAPI):
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

    responses.add(responses.POST, f"{API_BASE_URL}/tasks/{task_id}", status=204)

    response = todoist_api.update_task(
        task_id=task_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(responses.calls) == 1
    assert_auth_header(responses.calls[0].request)
    assert_request_id_header(responses.calls[0].request)
    assert responses.calls[0].request.body == json.dumps(args)
    assert response is True


@responses.activate
def test_close_task(todoist_api: TodoistAPI):
    task_id = 1234
    expected_endpoint = f"{API_BASE_URL}/tasks/{task_id}/close"

    responses.add(
        responses.POST,
        expected_endpoint,
        status=204,
    )

    response = todoist_api.close_task(task_id)

    assert len(responses.calls) == 1
    assert_auth_header(responses.calls[0].request)
    assert response is True


@responses.activate
def test_reopen_task(todoist_api: TodoistAPI):
    task_id = 1234
    expected_endpoint = f"{API_BASE_URL}/tasks/{task_id}/reopen"

    responses.add(
        responses.POST,
        expected_endpoint,
        status=204,
    )

    response = todoist_api.reopen_task(task_id)

    assert len(responses.calls) == 1
    assert_auth_header(responses.calls[0].request)
    assert response is True


@responses.activate
def test_delete_task(todoist_api: TodoistAPI):
    task_id = 1234
    expected_endpoint = f"{API_BASE_URL}/tasks/{task_id}"

    responses.add(
        responses.DELETE,
        expected_endpoint,
        status=204,
    )

    response = todoist_api.delete_task(task_id)

    assert len(responses.calls) == 1
    assert_auth_header(responses.calls[0].request)
    assert response is True
