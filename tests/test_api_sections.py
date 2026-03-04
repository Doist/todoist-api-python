from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import pytest

from tests.data.test_defaults import DEFAULT_API_URL, PaginatedResults
from tests.utils.test_utils import api_headers, enumerate_async, mock_route

if TYPE_CHECKING:
    import respx

    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Section


@pytest.mark.asyncio
async def test_get_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_section_response: dict[str, Any],
    default_section: Section,
) -> None:
    section_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/sections/{section_id}"

    mock_route(
        respx_mock,
        method="GET",
        url=endpoint,
        request_headers=api_headers(),
        response_json=default_section_response,
        response_status=200,
    )

    section = todoist_api.get_section(section_id)

    assert len(respx_mock.calls) == 1
    assert section == default_section

    section = await todoist_api_async.get_section(section_id)

    assert len(respx_mock.calls) == 2
    assert section == default_section


@pytest.mark.asyncio
async def test_get_sections(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_sections_response: list[PaginatedResults],
    default_sections_list: list[list[Section]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/sections"

    cursor: str | None = None
    for page in default_sections_response:
        mock_route(
            respx_mock,
            method="GET",
            url=endpoint,
            request_params={"cursor": cursor} if cursor else {},
            request_headers=api_headers(),
            response_json=page,
            response_status=200,
        )
        cursor = page["next_cursor"]

    count = 0

    sections_iter = todoist_api.get_sections()

    for i, sections in enumerate(sections_iter):
        assert len(respx_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1

    sections_async_iter = await todoist_api_async.get_sections()

    async for i, sections in enumerate_async(sections_async_iter):
        assert len(respx_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1


@pytest.mark.asyncio
async def test_get_sections_by_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_sections_response: list[PaginatedResults],
    default_sections_list: list[list[Section]],
) -> None:
    project_id = "123"
    endpoint = f"{DEFAULT_API_URL}/sections"

    cursor: str | None = None
    for page in default_sections_response:
        mock_route(
            respx_mock,
            method="GET",
            url=endpoint,
            request_params={"project_id": project_id}
            | ({"cursor": cursor} if cursor else {}),
            request_headers=api_headers(),
            response_json=page,
            response_status=200,
        )
        cursor = page["next_cursor"]

    count = 0

    sections_iter = todoist_api.get_sections(project_id=project_id)

    for i, sections in enumerate(sections_iter):
        assert len(respx_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1

    sections_async_iter = await todoist_api_async.get_sections(project_id=project_id)

    async for i, sections in enumerate_async(sections_async_iter):
        assert len(respx_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1


@pytest.mark.asyncio
async def test_search_sections(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_sections_response: list[PaginatedResults],
    default_sections_list: list[list[Section]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/sections/search"
    query = "A Section"

    cursor: str | None = None
    for page in default_sections_response:
        mock_route(
            respx_mock,
            method="GET",
            url=endpoint,
            request_params={"query": query} | ({"cursor": cursor} if cursor else {}),
            request_headers=api_headers(),
            response_json=page,
            response_status=200,
        )
        cursor = page["next_cursor"]

    count = 0

    sections_iter = todoist_api.search_sections(query)

    for i, sections in enumerate(sections_iter):
        assert len(respx_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1

    sections_async_iter = await todoist_api_async.search_sections(query)

    async for i, sections in enumerate_async(sections_async_iter):
        assert len(respx_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1


@pytest.mark.asyncio
async def test_search_sections_by_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_sections_response: list[PaginatedResults],
    default_sections_list: list[list[Section]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/sections/search"
    project_id = "123"
    query = "A Section"

    cursor: str | None = None
    for page in default_sections_response:
        mock_route(
            respx_mock,
            method="GET",
            url=endpoint,
            request_params={"query": query, "project_id": project_id}
            | ({"cursor": cursor} if cursor else {}),
            request_headers=api_headers(),
            response_json=page,
            response_status=200,
        )
        cursor = page["next_cursor"]

    count = 0

    sections_iter = todoist_api.search_sections(query, project_id=project_id)

    for i, sections in enumerate(sections_iter):
        assert len(respx_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1

    sections_async_iter = await todoist_api_async.search_sections(
        query, project_id=project_id
    )

    async for i, sections in enumerate_async(sections_async_iter):
        assert len(respx_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1


@pytest.mark.asyncio
async def test_add_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_section_response: dict[str, Any],
    default_section: Section,
) -> None:
    section_name = "A Section"
    project_id = "123"
    args = {
        "order": 3,
    }

    mock_route(
        respx_mock,
        method="POST",
        url=f"{DEFAULT_API_URL}/sections",
        request_headers=api_headers(),
        request_json={"name": section_name, "project_id": project_id} | args,
        response_json=default_section_response,
        response_status=200,
    )

    new_section = todoist_api.add_section(
        name=section_name, project_id=project_id, **args
    )

    assert len(respx_mock.calls) == 1
    assert new_section == default_section

    new_section = await todoist_api_async.add_section(
        name=section_name, project_id=project_id, **args
    )

    assert len(respx_mock.calls) == 2
    assert new_section == default_section


@pytest.mark.asyncio
async def test_update_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_section: Section,
    default_section_response: dict[str, Any],
) -> None:
    args: dict[str, Any] = {
        "name": "An updated section",
    }
    updated_section_response = dict(default_section_response) | args

    mock_route(
        respx_mock,
        method="POST",
        url=f"{DEFAULT_API_URL}/sections/{default_section.id}",
        request_headers=api_headers(),
        request_json=args,
        response_json=updated_section_response,
        response_status=200,
    )

    response = todoist_api.update_section(section_id=default_section.id, **args)

    assert len(respx_mock.calls) == 1
    assert response == Section.from_dict(updated_section_response)

    response = await todoist_api_async.update_section(
        section_id=default_section.id, **args
    )

    assert len(respx_mock.calls) == 2
    assert response == Section.from_dict(updated_section_response)


@pytest.mark.asyncio
async def test_update_section_payload_mapping(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_section: Section,
    default_section_response: dict[str, Any],
) -> None:
    args: dict[str, Any] = {
        "order": 2,
        "collapsed": False,
    }
    expected_payload: dict[str, Any] = {
        "section_order": 2,
        "is_collapsed": False,
    }
    updated_section_response = dict(default_section_response) | {
        "section_order": args["order"],
        "is_collapsed": args["collapsed"],
    }

    mock_route(
        respx_mock,
        method="POST",
        url=f"{DEFAULT_API_URL}/sections/{default_section.id}",
        request_headers=api_headers(),
        response_json=updated_section_response,
        response_status=200,
    )

    response = todoist_api.update_section(section_id=default_section.id, **args)

    assert len(respx_mock.calls) == 1
    assert response == Section.from_dict(updated_section_response)
    actual_payload = json.loads(respx_mock.calls[0].request.content)
    assert actual_payload == expected_payload

    response = await todoist_api_async.update_section(
        section_id=default_section.id, **args
    )

    assert len(respx_mock.calls) == 2
    assert response == Section.from_dict(updated_section_response)
    actual_payload = json.loads(respx_mock.calls[1].request.content)
    assert actual_payload == expected_payload


@pytest.mark.asyncio
async def test_delete_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
) -> None:
    section_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/sections/{section_id}"

    mock_route(
        respx_mock,
        method="DELETE",
        url=endpoint,
        request_headers=api_headers(),
        response_status=204,
    )

    response = todoist_api.delete_section(section_id)

    assert len(respx_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.delete_section(section_id)

    assert len(respx_mock.calls) == 2
    assert response is True
