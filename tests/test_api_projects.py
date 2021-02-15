import json
import typing
from typing import Any, Dict, List

import pytest
import responses

from tests.data.test_defaults import (
    DEFAULT_REQUEST_ID,
    INVALID_ENTITY_ID,
    REST_API_BASE_URL,
)
from tests.utils.test_utils import (
    assert_auth_header,
    assert_id_validation,
    assert_request_id_header,
)
from todoist_api_python.api import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Project


@pytest.mark.asyncio
async def test_get_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_project_response: Dict[str, Any],
    default_project: Project,
):
    project_id = 1234
    expected_endpoint = f"{REST_API_BASE_URL}/projects/{project_id}"

    requests_mock.add(
        responses.GET,
        expected_endpoint,
        json=default_project_response,
        status=200,
    )

    project = todoist_api.get_project(project_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert project == default_project

    project = await todoist_api_async.get_project(project_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert project == default_project


@typing.no_type_check
def test_get_project_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.get_project(INVALID_ENTITY_ID),
        requests_mock,
    )


@pytest.mark.asyncio
async def test_get_projects(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_projects_response: List[Dict[str, Any]],
    default_projects_list: List[Project],
):
    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}/projects",
        json=default_projects_response,
        status=200,
    )

    projects = todoist_api.get_projects()

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert projects == default_projects_list

    projects = await todoist_api_async.get_projects()

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert projects == default_projects_list


@pytest.mark.asyncio
async def test_add_project_minimal(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_project_response: Dict[str, Any],
    default_project: Project,
):
    project_name = "A Project"
    expected_payload = {"name": project_name}

    requests_mock.add(
        responses.POST,
        f"{REST_API_BASE_URL}/projects",
        json=default_project_response,
        status=200,
    )

    new_project = todoist_api.add_project(
        name=project_name, request_id=DEFAULT_REQUEST_ID
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(expected_payload)
    assert new_project == default_project

    new_project = await todoist_api_async.add_project(
        name=project_name, request_id=DEFAULT_REQUEST_ID
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(expected_payload)
    assert new_project == default_project


@pytest.mark.asyncio
async def test_add_project_full(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_project_response: Dict[str, Any],
    default_project: Project,
):
    project_name = "A Project"

    optional_args = {
        "parent_id": 789,
        "color": 30,
        "order": 3,
        "favorite": True,
    }

    expected_payload: Dict[str, Any] = {"name": project_name}
    expected_payload.update(optional_args)

    requests_mock.add(
        responses.POST,
        f"{REST_API_BASE_URL}/projects",
        json=default_project_response,
        status=200,
    )

    new_project = todoist_api.add_project(
        name=project_name, request_id=DEFAULT_REQUEST_ID, **optional_args
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(expected_payload)
    assert new_project == default_project

    new_project = await todoist_api_async.add_project(
        name=project_name, request_id=DEFAULT_REQUEST_ID, **optional_args
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(expected_payload)
    assert new_project == default_project


@pytest.mark.asyncio
async def test_update_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
):
    project_id = 123

    args = {
        "name": "An updated project",
        "color": 31,
        "favorite": False,
    }

    requests_mock.add(
        responses.POST, f"{REST_API_BASE_URL}/projects/{project_id}", status=204
    )

    response = todoist_api.update_project(
        project_id=project_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(args)
    assert response is True

    response = await todoist_api_async.update_project(
        project_id=project_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(args)
    assert response is True


@typing.no_type_check
def test_update_project_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.update_project(INVALID_ENTITY_ID),
        requests_mock,
    )


@pytest.mark.asyncio
async def test_delete_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
):
    project_id = 1234
    expected_endpoint = f"{REST_API_BASE_URL}/projects/{project_id}"

    requests_mock.add(
        responses.DELETE,
        expected_endpoint,
        status=204,
    )

    response = todoist_api.delete_project(project_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert response is True

    response = await todoist_api_async.delete_project(project_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert response is True


@typing.no_type_check
def test_delete_project_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.delete_project(INVALID_ENTITY_ID),
        requests_mock,
    )


@pytest.mark.asyncio
async def test_get_collaborators(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_collaborators_response: List[Dict[str, Any]],
    default_collaborators_list: List[Project],
):
    project_id = 123
    expected_endpoint = f"{REST_API_BASE_URL}/projects/{project_id}/collaborators"

    requests_mock.add(
        responses.GET,
        expected_endpoint,
        json=default_collaborators_response,
        status=200,
    )

    collaborators = todoist_api.get_collaborators(project_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert collaborators == default_collaborators_list

    collaborators = await todoist_api_async.get_collaborators(project_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert collaborators == default_collaborators_list


@typing.no_type_check
def test_get_collaborators_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.get_collaborators(INVALID_ENTITY_ID),
        requests_mock,
    )
