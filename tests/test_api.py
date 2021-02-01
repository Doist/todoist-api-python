import urllib
from typing import Any, Dict, List

import responses

from tests.conftest import DEFAULT_TOKEN
from todoist_api_python import TodoistAPI
from todoist_api_python.models import Task


def assert_auth_header(request):
    assert request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"


@responses.activate
def test_get_task(
    todoist_api: TodoistAPI, default_task_response: Dict[str, Any], default_task: Task
):
    task_id = 1234
    expected_endpoint = f"https://api.todoist.com/rest/v1/tasks/{task_id}"

    responses.add(
        responses.GET,
        expected_endpoint,
        json=default_task_response,
        status=200,
    )

    task = todoist_api.get_task(task_id)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == expected_endpoint
    assert_auth_header(responses.calls[0].request)
    assert task == default_task


@responses.activate
def test_get_tasks_minimal(
    todoist_api: TodoistAPI,
    default_tasks_response: List[Dict[str, Any]],
    default_tasks_list: List[Task],
):
    expected_endpoint = "https://api.todoist.com/rest/v1/tasks"

    responses.add(
        responses.GET, expected_endpoint, json=default_tasks_response, status=200
    )

    tasks = todoist_api.get_tasks()

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == expected_endpoint
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
        "https://api.todoist.com/rest/v1/tasks"
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
    assert responses.calls[0].request.url == expected_endpoint
    assert_auth_header(responses.calls[0].request)
    assert tasks == default_tasks_list
