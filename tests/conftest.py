from typing import Any, Dict, List

import pytest
import responses

from tests.data.quick_add_responses import QUICK_ADD_RESPONSE_FULL
from tests.data.test_defaults import (
    DEFAULT_COLLABORATORS_RESPONSE,
    DEFAULT_COMMENT_RESPONSE,
    DEFAULT_COMMENTS_RESPONSE,
    DEFAULT_LABEL_RESPONSE,
    DEFAULT_LABELS_RESPONSE,
    DEFAULT_PROJECT_RESPONSE,
    DEFAULT_PROJECTS_RESPONSE,
    DEFAULT_SECTION_RESPONSE,
    DEFAULT_SECTIONS_RESPONSE,
    DEFAULT_TASK_RESPONSE,
    DEFAULT_TASKS_RESPONSE,
    DEFAULT_TOKEN,
)
from todoist_api_python.api import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import (
    Collaborator,
    Comment,
    Label,
    Project,
    QuickAddResult,
    Section,
    Task,
)


@pytest.fixture()
def requests_mock() -> responses.RequestsMock:
    with responses.RequestsMock() as requestsMock:
        yield requestsMock


@pytest.fixture()
def todoist_api() -> TodoistAPI:
    return TodoistAPI(DEFAULT_TOKEN)


@pytest.fixture()
def todoist_api_async() -> TodoistAPIAsync:
    return TodoistAPIAsync(DEFAULT_TOKEN)


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


@pytest.fixture()
def default_project_response() -> Dict[str, Any]:
    return DEFAULT_PROJECT_RESPONSE


@pytest.fixture()
def default_project() -> Project:
    return Project.from_dict(DEFAULT_PROJECT_RESPONSE)


@pytest.fixture()
def default_projects_response() -> List[Dict[str, Any]]:
    return DEFAULT_PROJECTS_RESPONSE


@pytest.fixture()
def default_projects_list() -> List[Project]:
    return [Project.from_dict(obj) for obj in DEFAULT_PROJECTS_RESPONSE]


@pytest.fixture()
def default_collaborators_response() -> List[Dict[str, Any]]:
    return DEFAULT_COLLABORATORS_RESPONSE


@pytest.fixture()
def default_collaborators_list() -> List[Collaborator]:
    return [Collaborator.from_dict(obj) for obj in DEFAULT_COLLABORATORS_RESPONSE]


@pytest.fixture()
def default_section_response() -> Dict[str, Any]:
    return DEFAULT_SECTION_RESPONSE


@pytest.fixture()
def default_section() -> Section:
    return Section.from_dict(DEFAULT_SECTION_RESPONSE)


@pytest.fixture()
def default_sections_response() -> List[Dict[str, Any]]:
    return DEFAULT_SECTIONS_RESPONSE


@pytest.fixture()
def default_sections_list() -> List[Section]:
    return [Section.from_dict(obj) for obj in DEFAULT_SECTIONS_RESPONSE]


@pytest.fixture()
def default_comment_response() -> Dict[str, Any]:
    return DEFAULT_COMMENT_RESPONSE


@pytest.fixture()
def default_comment() -> Comment:
    return Comment.from_dict(DEFAULT_COMMENT_RESPONSE)


@pytest.fixture()
def default_comments_response() -> List[Dict[str, Any]]:
    return DEFAULT_COMMENTS_RESPONSE


@pytest.fixture()
def default_comments_list() -> List[Comment]:
    return [Comment.from_dict(obj) for obj in DEFAULT_COMMENTS_RESPONSE]


@pytest.fixture()
def default_label_response() -> Dict[str, Any]:
    return DEFAULT_LABEL_RESPONSE


@pytest.fixture()
def default_label() -> Label:
    return Label.from_dict(DEFAULT_LABEL_RESPONSE)


@pytest.fixture()
def default_labels_response() -> List[Dict[str, Any]]:
    return DEFAULT_LABELS_RESPONSE


@pytest.fixture()
def default_labels_list() -> List[Label]:
    return [Label.from_dict(obj) for obj in DEFAULT_LABELS_RESPONSE]


@pytest.fixture()
def default_quick_add_response() -> Dict[str, Any]:
    return QUICK_ADD_RESPONSE_FULL


@pytest.fixture()
def default_quick_add_result() -> QuickAddResult:
    return QuickAddResult.from_quick_add_response(QUICK_ADD_RESPONSE_FULL)
