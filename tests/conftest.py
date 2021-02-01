from typing import Any, Dict, List

import pytest

from tests.data.test_defaults import (
    DEFAULT_TASK_RESPONSE,
    DEFAULT_TASKS_RESPONSE,
    DEFAULT_TOKEN,
)
from todoist_api_python import TodoistAPI
from todoist_api_python.models import Task


@pytest.fixture()
def todoist_api() -> TodoistAPI:
    return TodoistAPI(DEFAULT_TOKEN)


@pytest.fixture()
def default_task_response() -> Dict[str, Any]:
    return DEFAULT_TASK_RESPONSE


@pytest.fixture()
def default_task() -> Task:
    return Task.from_dict(DEFAULT_TASK_RESPONSE)


@pytest.fixture()
def default_tasks_response() -> List[Dict[str, Any]]:
    return DEFAULT_TASKS_RESPONSE


@pytest.fixture()
def default_tasks_list() -> List[Task]:
    return [Task.from_dict(obj) for obj in DEFAULT_TASKS_RESPONSE]
