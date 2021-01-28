import urllib

import responses

from tests.conftest import DEFAULT_TOKEN
from tests.data.test_defaults import (
    DEFAULT_TASK,
    DEFAULT_TASK_DATA,
    DEFAULT_TASKS_DATA,
    DEFAULT_TASKS_LIST,
)
from todoist_api_python import TodoistAPI


def assert_auth_header(request):
    assert request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"


@responses.activate
def test_get_task(todoist_api: TodoistAPI):
    task_id = 1234
    expected_endpoint = f"https://api.todoist.com/rest/v1/tasks/{task_id}"

    responses.add(
        responses.GET,
        expected_endpoint,
        json=DEFAULT_TASK_DATA,
        status=200,
    )

    task = todoist_api.get_task(task_id)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == expected_endpoint
    assert_auth_header(responses.calls[0].request)
    assert task == DEFAULT_TASK


@responses.activate
def test_get_tasks_minimal(todoist_api: TodoistAPI):
    expected_endpoint = "https://api.todoist.com/rest/v1/tasks"

    responses.add(responses.GET, expected_endpoint, json=DEFAULT_TASKS_DATA, status=200)

    tasks = todoist_api.get_tasks()

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == expected_endpoint
    assert_auth_header(responses.calls[0].request)
    assert tasks == DEFAULT_TASKS_LIST


@responses.activate
def test_get_tasks_full(todoist_api: TodoistAPI):
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

    responses.add(responses.GET, expected_endpoint, json=DEFAULT_TASKS_DATA, status=200)

    tasks = todoist_api.get_tasks(
        project_id=project_id, label_id=label_id, filter=filter, lang=lang, ids=ids
    )

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == expected_endpoint
    assert_auth_header(responses.calls[0].request)
    assert tasks == DEFAULT_TASKS_LIST
