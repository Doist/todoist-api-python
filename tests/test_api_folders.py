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
from todoist_api_python.models import Folder


@pytest.mark.asyncio
async def test_get_folder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_folder_response: dict[str, Any],
    default_folder: Folder,
) -> None:
    folder_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/folders/{folder_id}"

    requests_mock.add(
        method=responses.GET,
        url=endpoint,
        json=default_folder_response,
        status=200,
        match=[auth_matcher()],
    )

    folder = todoist_api.get_folder(folder_id)

    assert len(requests_mock.calls) == 1
    assert folder == default_folder

    folder = await todoist_api_async.get_folder(folder_id)

    assert len(requests_mock.calls) == 2
    assert folder == default_folder


@pytest.mark.asyncio
async def test_get_folders(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_folders_response: list[PaginatedResults],
    default_folders_list: list[list[Folder]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/folders"

    cursor: str | None = None
    for page in default_folders_response:
        requests_mock.add(
            method=responses.GET,
            url=endpoint,
            json=page,
            status=200,
            match=[auth_matcher(), request_id_matcher(), param_matcher({}, cursor)],
        )
        cursor = page["next_cursor"]

    count = 0

    folders_iter = todoist_api.get_folders()

    for i, folders in enumerate(folders_iter):
        assert len(requests_mock.calls) == count + 1
        assert folders == default_folders_list[i]
        count += 1

    folders_async_iter = await todoist_api_async.get_folders()

    async for i, folders in enumerate_async(folders_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert folders == default_folders_list[i]
        count += 1


@pytest.mark.asyncio
async def test_get_folders_with_workspace_id(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_folders_response: list[PaginatedResults],
    default_folders_list: list[list[Folder]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/folders"
    workspace_id = "ws_001"

    cursor: str | None = None
    for page in default_folders_response:
        requests_mock.add(
            method=responses.GET,
            url=endpoint,
            json=page,
            status=200,
            match=[
                auth_matcher(),
                request_id_matcher(),
                param_matcher({"workspace_id": workspace_id}, cursor),
            ],
        )
        cursor = page["next_cursor"]

    count = 0

    folders_iter = todoist_api.get_folders(workspace_id=workspace_id)

    for i, folders in enumerate(folders_iter):
        assert len(requests_mock.calls) == count + 1
        assert folders == default_folders_list[i]
        count += 1

    folders_async_iter = await todoist_api_async.get_folders(
        workspace_id=workspace_id,
    )

    async for i, folders in enumerate_async(folders_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert folders == default_folders_list[i]
        count += 1


@pytest.mark.asyncio
async def test_add_folder_minimal(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_folder_response: dict[str, Any],
    default_folder: Folder,
) -> None:
    folder_name = "Test Folder"
    workspace_id = "ws_001"

    requests_mock.add(
        method=responses.POST,
        url=f"{DEFAULT_API_URL}/folders",
        json=default_folder_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher({"name": folder_name, "workspace_id": workspace_id}),
        ],
    )

    new_folder = todoist_api.add_folder(name=folder_name, workspace_id=workspace_id)

    assert len(requests_mock.calls) == 1
    assert new_folder == default_folder

    new_folder = await todoist_api_async.add_folder(
        name=folder_name, workspace_id=workspace_id
    )

    assert len(requests_mock.calls) == 2
    assert new_folder == default_folder


@pytest.mark.asyncio
async def test_add_folder_full(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_folder_response: dict[str, Any],
    default_folder: Folder,
) -> None:
    folder_name = "Test Folder"
    workspace_id = "ws_001"
    default_order = 1
    child_order = 2

    requests_mock.add(
        method=responses.POST,
        url=f"{DEFAULT_API_URL}/folders",
        json=default_folder_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher(
                {
                    "name": folder_name,
                    "workspace_id": workspace_id,
                    "default_order": default_order,
                    "child_order": child_order,
                }
            ),
        ],
    )

    new_folder = todoist_api.add_folder(
        name=folder_name,
        workspace_id=workspace_id,
        default_order=default_order,
        child_order=child_order,
    )

    assert len(requests_mock.calls) == 1
    assert new_folder == default_folder

    new_folder = await todoist_api_async.add_folder(
        name=folder_name,
        workspace_id=workspace_id,
        default_order=default_order,
        child_order=child_order,
    )

    assert len(requests_mock.calls) == 2
    assert new_folder == default_folder


@pytest.mark.asyncio
async def test_update_folder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_folder: Folder,
) -> None:
    args: dict[str, Any] = {
        "name": "Updated Folder",
        "default_order": 5,
    }
    updated_folder_dict = default_folder.to_dict() | args

    requests_mock.add(
        method=responses.POST,
        url=f"{DEFAULT_API_URL}/folders/{default_folder.id}",
        json=updated_folder_dict,
        status=200,
        match=[auth_matcher(), request_id_matcher(), data_matcher(args)],
    )

    response = todoist_api.update_folder(folder_id=default_folder.id, **args)

    assert len(requests_mock.calls) == 1
    assert response == Folder.from_dict(updated_folder_dict)

    response = await todoist_api_async.update_folder(
        folder_id=default_folder.id, **args
    )

    assert len(requests_mock.calls) == 2
    assert response == Folder.from_dict(updated_folder_dict)


@pytest.mark.asyncio
async def test_delete_folder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
) -> None:
    folder_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/folders/{folder_id}"

    requests_mock.add(
        method=responses.DELETE,
        url=endpoint,
        status=204,
        match=[auth_matcher(), request_id_matcher()],
    )

    response = todoist_api.delete_folder(folder_id)

    assert len(requests_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.delete_folder(folder_id)

    assert len(requests_mock.calls) == 2
    assert response is True
