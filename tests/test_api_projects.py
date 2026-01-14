from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
import responses

from tests.data.test_defaults import DEFAULT_API_URL, PaginatedResults
from tests.utils.test_utils import (
    auth_matcher,
    data_matcher,
    enumerate_async,
    param_matcher,
    request_id_matcher,
)

if TYPE_CHECKING:
    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Collaborator, Project


@pytest.mark.asyncio
async def test_get_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_project_response: dict[str, Any],
    default_project: Project,
) -> None:
    project_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/projects/{project_id}"

    requests_mock.add(
        method=responses.GET,
        url=endpoint,
        json=default_project_response,
        status=200,
        match=[auth_matcher()],
    )

    project = todoist_api.get_project(project_id)

    assert len(requests_mock.calls) == 1
    assert project == default_project

    project = await todoist_api_async.get_project(project_id)

    assert len(requests_mock.calls) == 2
    assert project == default_project


@pytest.mark.asyncio
async def test_get_projects(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_projects_response: list[PaginatedResults],
    default_projects_list: list[list[Project]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/projects"

    cursor: str | None = None
    for page in default_projects_response:
        requests_mock.add(
            method=responses.GET,
            url=endpoint,
            json=page,
            status=200,
            match=[auth_matcher(), request_id_matcher(), param_matcher({}, cursor)],
        )
        cursor = page["next_cursor"]

    count = 0

    projects_iter = todoist_api.get_projects()

    for i, projects in enumerate(projects_iter):
        assert len(requests_mock.calls) == count + 1
        assert projects == default_projects_list[i]
        count += 1

    projects_async_iter = await todoist_api_async.get_projects()

    async for i, projects in enumerate_async(projects_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert projects == default_projects_list[i]
        count += 1


@pytest.mark.asyncio
async def test_search_projects(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_projects_response: list[PaginatedResults],
    default_projects_list: list[list[Project]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/projects/search"
    query = "Inbox"

    cursor: str | None = None
    for page in default_projects_response:
        requests_mock.add(
            method=responses.GET,
            url=endpoint,
            json=page,
            status=200,
            match=[
                auth_matcher(),
                request_id_matcher(),
                param_matcher({"query": query}, cursor),
            ],
        )
        cursor = page["next_cursor"]

    count = 0

    projects_iter = todoist_api.search_projects(query)

    for i, projects in enumerate(projects_iter):
        assert len(requests_mock.calls) == count + 1
        assert projects == default_projects_list[i]
        count += 1

    projects_async_iter = await todoist_api_async.search_projects(query)

    async for i, projects in enumerate_async(projects_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert projects == default_projects_list[i]
        count += 1


@pytest.mark.asyncio
async def test_add_project_minimal(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_project_response: dict[str, Any],
    default_project: Project,
) -> None:
    project_name = "A Project"

    requests_mock.add(
        method=responses.POST,
        url=f"{DEFAULT_API_URL}/projects",
        json=default_project_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher({"name": project_name}),
        ],
    )

    new_project = todoist_api.add_project(name=project_name)

    assert len(requests_mock.calls) == 1
    assert new_project == default_project

    new_project = await todoist_api_async.add_project(name=project_name)

    assert len(requests_mock.calls) == 2
    assert new_project == default_project


@pytest.mark.asyncio
async def test_add_project_full(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_project_response: dict[str, Any],
    default_project: Project,
) -> None:
    project_name = "A Project"

    requests_mock.add(
        method=responses.POST,
        url=f"{DEFAULT_API_URL}/projects",
        json=default_project_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher({"name": project_name}),
        ],
    )

    new_project = todoist_api.add_project(name=project_name)

    assert len(requests_mock.calls) == 1
    assert new_project == default_project

    new_project = await todoist_api_async.add_project(name=project_name)

    assert len(requests_mock.calls) == 2
    assert new_project == default_project


@pytest.mark.asyncio
async def test_update_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_project: Project,
) -> None:
    args: dict[str, Any] = {
        "name": "An updated project",
        "color": "red",
        "is_favorite": False,
    }
    updated_project_dict = default_project.to_dict() | args

    requests_mock.add(
        method=responses.POST,
        url=f"{DEFAULT_API_URL}/projects/{default_project.id}",
        json=updated_project_dict,
        status=200,
        match=[auth_matcher(), request_id_matcher(), data_matcher(args)],
    )

    response = todoist_api.update_project(project_id=default_project.id, **args)

    assert len(requests_mock.calls) == 1
    assert response == Project.from_dict(updated_project_dict)

    response = await todoist_api_async.update_project(
        project_id=default_project.id, **args
    )

    assert len(requests_mock.calls) == 2
    assert response == Project.from_dict(updated_project_dict)


@pytest.mark.asyncio
async def test_archive_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_project: Project,
) -> None:
    project_id = default_project.id
    endpoint = f"{DEFAULT_API_URL}/projects/{project_id}/archive"

    archived_project_dict = default_project.to_dict()
    archived_project_dict["is_archived"] = True

    requests_mock.add(
        method=responses.POST,
        url=endpoint,
        json=archived_project_dict,
        status=200,
        match=[auth_matcher(), request_id_matcher()],
    )

    project = todoist_api.archive_project(project_id)

    assert len(requests_mock.calls) == 1
    assert project == Project.from_dict(archived_project_dict)

    project = await todoist_api_async.archive_project(project_id)

    assert len(requests_mock.calls) == 2
    assert project == Project.from_dict(archived_project_dict)


@pytest.mark.asyncio
async def test_unarchive_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_project: Project,
) -> None:
    project_id = default_project.id
    endpoint = f"{DEFAULT_API_URL}/projects/{project_id}/unarchive"

    unarchived_project_dict = default_project.to_dict()
    unarchived_project_dict["is_archived"] = False

    requests_mock.add(
        method=responses.POST,
        url=endpoint,
        json=unarchived_project_dict,
        status=200,
        match=[auth_matcher(), request_id_matcher()],
    )

    project = todoist_api.unarchive_project(project_id)

    assert len(requests_mock.calls) == 1
    assert project == Project.from_dict(unarchived_project_dict)

    project = await todoist_api_async.unarchive_project(project_id)

    assert len(requests_mock.calls) == 2
    assert project == Project.from_dict(unarchived_project_dict)


@pytest.mark.asyncio
async def test_delete_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
) -> None:
    project_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/projects/{project_id}"

    requests_mock.add(
        method=responses.DELETE,
        url=endpoint,
        status=204,
        match=[auth_matcher(), request_id_matcher()],
    )

    response = todoist_api.delete_project(project_id)

    assert len(requests_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.delete_project(project_id)

    assert len(requests_mock.calls) == 2
    assert response is True


@pytest.mark.asyncio
async def test_get_collaborators(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_collaborators_response: list[PaginatedResults],
    default_collaborators_list: list[list[Collaborator]],
) -> None:
    project_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/projects/{project_id}/collaborators"

    cursor: str | None = None
    for page in default_collaborators_response:
        requests_mock.add(
            method=responses.GET,
            url=endpoint,
            json=page,
            status=200,
            match=[auth_matcher(), request_id_matcher(), param_matcher({}, cursor)],
        )
        cursor = page["next_cursor"]

    count = 0

    collaborators_iter = todoist_api.get_collaborators(project_id)

    for i, collaborators in enumerate(collaborators_iter):
        assert len(requests_mock.calls) == count + 1
        assert collaborators == default_collaborators_list[i]
        count += 1

    collaborators_async_iter = await todoist_api_async.get_collaborators(project_id)

    async for i, collaborators in enumerate_async(collaborators_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert collaborators == default_collaborators_list[i]
        count += 1
