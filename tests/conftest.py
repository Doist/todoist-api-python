from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
import pytest_asyncio

from tests.data.test_defaults import (
    DEFAULT_AUTH_RESPONSE,
    DEFAULT_COLLABORATORS_RESPONSE,
    DEFAULT_COMMENT_RESPONSE,
    DEFAULT_COMMENTS_RESPONSE,
    DEFAULT_COMPLETED_TASKS_RESPONSE,
    DEFAULT_LABEL_RESPONSE,
    DEFAULT_LABELS_RESPONSE,
    DEFAULT_PROJECT_RESPONSE,
    DEFAULT_PROJECTS_RESPONSE,
    DEFAULT_SECTION_RESPONSE,
    DEFAULT_SECTIONS_RESPONSE,
    DEFAULT_TASK_META_RESPONSE,
    DEFAULT_TASK_RESPONSE,
    DEFAULT_TASKS_RESPONSE,
    DEFAULT_TOKEN,
    PaginatedItems,
    PaginatedResults,
)
from todoist_api_python.api import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import (
    AuthResult,
    Collaborator,
    Comment,
    Label,
    Project,
    Section,
    Task,
)

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator


@pytest.fixture
def todoist_api() -> Iterator[TodoistAPI]:
    with TodoistAPI(DEFAULT_TOKEN) as api:
        yield api


@pytest_asyncio.fixture
async def todoist_api_async() -> AsyncIterator[TodoistAPIAsync]:
    async with TodoistAPIAsync(DEFAULT_TOKEN) as api:
        yield api


@pytest.fixture
def default_task_response() -> dict[str, Any]:
    return DEFAULT_TASK_RESPONSE


@pytest.fixture
def default_task_meta() -> Task:
    return Task.from_dict(DEFAULT_TASK_META_RESPONSE)


@pytest.fixture
def default_task_meta_response() -> dict[str, Any]:
    return DEFAULT_TASK_META_RESPONSE


@pytest.fixture
def default_task() -> Task:
    return Task.from_dict(DEFAULT_TASK_RESPONSE)


@pytest.fixture
def default_tasks_response() -> list[PaginatedResults]:
    return DEFAULT_TASKS_RESPONSE


@pytest.fixture
def default_tasks_list() -> list[list[Task]]:
    return [
        [Task.from_dict(result) for result in response["results"]]
        for response in DEFAULT_TASKS_RESPONSE
    ]


@pytest.fixture
def default_completed_tasks_response() -> list[PaginatedItems]:
    return DEFAULT_COMPLETED_TASKS_RESPONSE


@pytest.fixture
def default_completed_tasks_list() -> list[list[Task]]:
    return [
        [Task.from_dict(result) for result in response["items"]]
        for response in DEFAULT_COMPLETED_TASKS_RESPONSE
    ]


@pytest.fixture
def default_project_response() -> dict[str, Any]:
    return DEFAULT_PROJECT_RESPONSE


@pytest.fixture
def default_project() -> Project:
    return Project.from_dict(DEFAULT_PROJECT_RESPONSE)


@pytest.fixture
def default_projects_response() -> list[PaginatedResults]:
    return DEFAULT_PROJECTS_RESPONSE


@pytest.fixture
def default_projects_list() -> list[list[Project]]:
    return [
        [Project.from_dict(result) for result in response["results"]]
        for response in DEFAULT_PROJECTS_RESPONSE
    ]


@pytest.fixture
def default_collaborators_response() -> list[PaginatedResults]:
    return DEFAULT_COLLABORATORS_RESPONSE


@pytest.fixture
def default_collaborators_list() -> list[list[Collaborator]]:
    return [
        [Collaborator.from_dict(result) for result in response["results"]]
        for response in DEFAULT_COLLABORATORS_RESPONSE
    ]


@pytest.fixture
def default_section_response() -> dict[str, Any]:
    return DEFAULT_SECTION_RESPONSE


@pytest.fixture
def default_section() -> Section:
    return Section.from_dict(DEFAULT_SECTION_RESPONSE)


@pytest.fixture
def default_sections_response() -> list[PaginatedResults]:
    return DEFAULT_SECTIONS_RESPONSE


@pytest.fixture
def default_sections_list() -> list[list[Section]]:
    return [
        [Section.from_dict(result) for result in response["results"]]
        for response in DEFAULT_SECTIONS_RESPONSE
    ]


@pytest.fixture
def default_comment_response() -> dict[str, Any]:
    return DEFAULT_COMMENT_RESPONSE


@pytest.fixture
def default_comment() -> Comment:
    return Comment.from_dict(DEFAULT_COMMENT_RESPONSE)


@pytest.fixture
def default_comments_response() -> list[PaginatedResults]:
    return DEFAULT_COMMENTS_RESPONSE


@pytest.fixture
def default_comments_list() -> list[list[Comment]]:
    return [
        [Comment.from_dict(result) for result in response["results"]]
        for response in DEFAULT_COMMENTS_RESPONSE
    ]


@pytest.fixture
def default_label_response() -> dict[str, Any]:
    return DEFAULT_LABEL_RESPONSE


@pytest.fixture
def default_label() -> Label:
    return Label.from_dict(DEFAULT_LABEL_RESPONSE)


@pytest.fixture
def default_labels_response() -> list[PaginatedResults]:
    return DEFAULT_LABELS_RESPONSE


@pytest.fixture
def default_labels_list() -> list[list[Label]]:
    return [
        [Label.from_dict(result) for result in response["results"]]
        for response in DEFAULT_LABELS_RESPONSE
    ]


@pytest.fixture
def default_quick_add_response() -> dict[str, Any]:
    return DEFAULT_TASK_RESPONSE


@pytest.fixture
def default_quick_add_result() -> Task:
    return Task.from_dict(DEFAULT_TASK_RESPONSE)


@pytest.fixture
def default_auth_response() -> dict[str, Any]:
    return DEFAULT_AUTH_RESPONSE


@pytest.fixture
def default_auth_result() -> AuthResult:
    return AuthResult.from_dict(DEFAULT_AUTH_RESPONSE)
