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
from todoist_api_python.models import Section


@pytest.mark.asyncio
async def test_get_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_section_response: dict[str, Any],
    default_section: Section,
) -> None:
    section_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/sections/{section_id}"

    requests_mock.add(
        method=responses.GET,
        url=endpoint,
        json=default_section_response,
        status=200,
        match=[auth_matcher()],
    )

    section = todoist_api.get_section(section_id)

    assert len(requests_mock.calls) == 1
    assert section == default_section

    section = await todoist_api_async.get_section(section_id)

    assert len(requests_mock.calls) == 2
    assert section == default_section


@pytest.mark.asyncio
async def test_get_sections(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_sections_response: list[PaginatedResults],
    default_sections_list: list[list[Section]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/sections"

    cursor: str | None = None
    for page in default_sections_response:
        requests_mock.add(
            method=responses.GET,
            url=endpoint,
            json=page,
            status=200,
            match=[auth_matcher(), request_id_matcher(), param_matcher({}, cursor)],
        )
        cursor = page["next_cursor"]

    count = 0

    sections_iter = todoist_api.get_sections()

    for i, sections in enumerate(sections_iter):
        assert len(requests_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1

    sections_async_iter = await todoist_api_async.get_sections()

    async for i, sections in enumerate_async(sections_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1


@pytest.mark.asyncio
async def test_get_sections_by_project(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_sections_response: list[PaginatedResults],
    default_sections_list: list[list[Section]],
) -> None:
    project_id = "123"
    endpoint = f"{DEFAULT_API_URL}/sections"

    cursor: str | None = None
    for page in default_sections_response:
        requests_mock.add(
            method=responses.GET,
            url=endpoint,
            json=page,
            status=200,
            match=[
                auth_matcher(),
                request_id_matcher(),
                param_matcher({"project_id": project_id}, cursor),
            ],
        )
        cursor = page["next_cursor"]

    count = 0

    sections_iter = todoist_api.get_sections(project_id=project_id)

    for i, sections in enumerate(sections_iter):
        assert len(requests_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1

    sections_async_iter = await todoist_api_async.get_sections(project_id=project_id)

    async for i, sections in enumerate_async(sections_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert sections == default_sections_list[i]
        count += 1


@pytest.mark.asyncio
async def test_add_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_section_response: dict[str, Any],
    default_section: Section,
) -> None:
    section_name = "A Section"
    project_id = "123"
    args = {
        "order": 3,
    }

    requests_mock.add(
        method=responses.POST,
        url=f"{DEFAULT_API_URL}/sections",
        json=default_section_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher({"name": section_name, "project_id": project_id} | args),
        ],
    )

    new_section = todoist_api.add_section(
        name=section_name, project_id=project_id, **args
    )

    assert len(requests_mock.calls) == 1
    assert new_section == default_section

    new_section = await todoist_api_async.add_section(
        name=section_name, project_id=project_id, **args
    )

    assert len(requests_mock.calls) == 2
    assert new_section == default_section


@pytest.mark.asyncio
async def test_update_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_section: Section,
) -> None:
    args = {
        "name": "An updated section",
    }
    updated_section_dict = default_section.to_dict() | args

    requests_mock.add(
        method=responses.POST,
        url=f"{DEFAULT_API_URL}/sections/{default_section.id}",
        json=updated_section_dict,
        status=200,
        match=[auth_matcher(), request_id_matcher(), data_matcher(args)],
    )

    response = todoist_api.update_section(section_id=default_section.id, **args)

    assert len(requests_mock.calls) == 1
    assert response == Section.from_dict(updated_section_dict)

    response = await todoist_api_async.update_section(
        section_id=default_section.id, **args
    )

    assert len(requests_mock.calls) == 2
    assert response == Section.from_dict(updated_section_dict)


@pytest.mark.asyncio
async def test_delete_section(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
) -> None:
    section_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/sections/{section_id}"

    requests_mock.add(
        method=responses.DELETE,
        url=endpoint,
        status=204,
        match=[auth_matcher(), request_id_matcher()],
    )

    response = todoist_api.delete_section(section_id)

    assert len(requests_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.delete_section(section_id)

    assert len(requests_mock.calls) == 2
    assert response is True
