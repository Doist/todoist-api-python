import json
from typing import Any, Dict, List

import pytest
import responses

from tests.data.test_defaults import DEFAULT_REQUEST_ID, REST_API_BASE_URL
from tests.utils.test_utils import assert_auth_header, assert_request_id_header
from todoist_api_python.api import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Section


@pytest.mark.asyncio
async def test_get_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_section_response: Dict[str, Any],
    default_section: Section,
):
    section_id = 1234
    expected_endpoint = f"{REST_API_BASE_URL}/sections/{section_id}"

    requests_mock.add(
        responses.GET,
        expected_endpoint,
        json=default_section_response,
        status=200,
    )

    section = todoist_api.get_section(section_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert section == default_section

    section = await todoist_api_async.get_section(section_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert section == default_section


@pytest.mark.asyncio
async def test_get_all_sections(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_sections_response: List[Dict[str, Any]],
    default_sections_list: List[Section],
):
    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}/sections",
        json=default_sections_response,
        status=200,
    )

    sections = todoist_api.get_sections()

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert sections == default_sections_list

    sections = await todoist_api_async.get_sections()

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert sections == default_sections_list


@pytest.mark.asyncio
async def test_get_project_sections(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_sections_response: List[Dict[str, Any]],
):
    project_id = 123

    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}/sections?project_id={project_id}",
        json=default_sections_response,
        status=200,
    )

    todoist_api.get_sections(project_id=project_id)
    await todoist_api_async.get_sections(project_id=project_id)

    assert len(requests_mock.calls) == 2


@pytest.mark.asyncio
async def test_add_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_section_response: Dict[str, Any],
    default_section: Section,
):
    section_name = "A Section"
    project_id = 123
    order = 3

    expected_payload: Dict[str, Any] = {
        "name": section_name,
        "project_id": project_id,
        "order": order,
    }

    requests_mock.add(
        responses.POST,
        f"{REST_API_BASE_URL}/sections",
        json=default_section_response,
        status=200,
    )

    new_section = todoist_api.add_section(
        name=section_name,
        project_id=project_id,
        order=order,
        request_id=DEFAULT_REQUEST_ID,
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(expected_payload)
    assert new_section == default_section

    new_section = await todoist_api_async.add_section(
        name=section_name,
        project_id=project_id,
        order=order,
        request_id=DEFAULT_REQUEST_ID,
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(expected_payload)
    assert new_section == default_section


@pytest.mark.asyncio
async def test_update_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
):
    section_id = 123

    args = {
        "name": "An updated section",
    }

    requests_mock.add(
        responses.POST, f"{REST_API_BASE_URL}/sections/{section_id}", status=204
    )

    response = todoist_api.update_section(
        section_id=section_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(args)
    assert response is True

    response = await todoist_api_async.update_section(
        section_id=section_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(args)
    assert response is True


@pytest.mark.asyncio
async def test_delete_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
):
    section_id = 1234
    expected_endpoint = f"{REST_API_BASE_URL}/sections/{section_id}"

    requests_mock.add(
        responses.DELETE,
        expected_endpoint,
        status=204,
    )

    response = todoist_api.delete_section(section_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert response is True

    response = await todoist_api_async.delete_section(section_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert response is True
