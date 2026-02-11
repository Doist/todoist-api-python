from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from tests.data.test_defaults import DEFAULT_API_URL, PaginatedResults
from tests.utils.test_utils import (
    auth_matcher,
    data_matcher,
    enumerate_async,
    param_matcher,
    request_id_matcher,
)

if TYPE_CHECKING:
    from tests.utils.http_mock import RequestsMock
    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Label


@pytest.mark.asyncio
async def test_get_label(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_label_response: dict[str, Any],
    default_label: Label,
) -> None:
    label_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/labels/{label_id}"

    requests_mock.add(
        method="GET",
        url=endpoint,
        json=default_label_response,
        status=200,
        match=[auth_matcher()],
    )

    label = todoist_api.get_label(label_id)

    assert len(requests_mock.calls) == 1
    assert label == default_label

    label = await todoist_api_async.get_label(label_id)

    assert len(requests_mock.calls) == 2
    assert label == default_label


@pytest.mark.asyncio
async def test_get_labels(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_labels_response: list[PaginatedResults],
    default_labels_list: list[list[Label]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/labels"

    cursor: str | None = None
    for page in default_labels_response:
        requests_mock.add(
            method="GET",
            url=endpoint,
            json=page,
            status=200,
            match=[auth_matcher(), request_id_matcher(), param_matcher({}, cursor)],
        )
        cursor = page["next_cursor"]

    count = 0

    labels_iter = todoist_api.get_labels()

    for i, labels in enumerate(labels_iter):
        assert len(requests_mock.calls) == count + 1
        assert labels == default_labels_list[i]
        count += 1

    labels_async_iter = await todoist_api_async.get_labels()

    async for i, labels in enumerate_async(labels_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert labels == default_labels_list[i]
        count += 1


@pytest.mark.asyncio
async def test_search_labels(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_labels_response: list[PaginatedResults],
    default_labels_list: list[list[Label]],
) -> None:
    endpoint = f"{DEFAULT_API_URL}/labels/search"
    query = "A label"

    cursor: str | None = None
    for page in default_labels_response:
        requests_mock.add(
            method="GET",
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

    labels_iter = todoist_api.search_labels(query)

    for i, labels in enumerate(labels_iter):
        assert len(requests_mock.calls) == count + 1
        assert labels == default_labels_list[i]
        count += 1

    labels_async_iter = await todoist_api_async.search_labels(query)

    async for i, labels in enumerate_async(labels_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert labels == default_labels_list[i]
        count += 1


@pytest.mark.asyncio
async def test_add_label_minimal(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_label_response: dict[str, Any],
    default_label: Label,
) -> None:
    label_name = "A Label"

    requests_mock.add(
        method="POST",
        url=f"{DEFAULT_API_URL}/labels",
        json=default_label_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher({"name": label_name}),
        ],
    )

    new_label = todoist_api.add_label(name=label_name)

    assert len(requests_mock.calls) == 1
    assert new_label == default_label

    new_label = await todoist_api_async.add_label(name=label_name)

    assert len(requests_mock.calls) == 2
    assert new_label == default_label


@pytest.mark.asyncio
async def test_add_label_full(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_label_response: dict[str, Any],
    default_label: Label,
) -> None:
    label_name = "A Label"
    args: dict[str, Any] = {
        "color": "red",
        "item_order": 3,
        "is_favorite": True,
    }

    requests_mock.add(
        method="POST",
        url=f"{DEFAULT_API_URL}/labels",
        json=default_label_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher({"name": label_name} | args),
        ],
    )

    new_label = todoist_api.add_label(name=label_name, **args)

    assert len(requests_mock.calls) == 1
    assert new_label == default_label

    new_label = await todoist_api_async.add_label(name=label_name, **args)

    assert len(requests_mock.calls) == 2
    assert new_label == default_label


@pytest.mark.asyncio
async def test_update_label(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_label: Label,
) -> None:
    args: dict[str, Any] = {
        "name": "An updated label",
    }
    updated_label_dict = default_label.to_dict() | args

    requests_mock.add(
        method="POST",
        url=f"{DEFAULT_API_URL}/labels/{default_label.id}",
        json=updated_label_dict,
        status=200,
        match=[auth_matcher(), request_id_matcher(), data_matcher(args)],
    )

    response = todoist_api.update_label(label_id=default_label.id, **args)

    assert len(requests_mock.calls) == 1
    assert response == Label.from_dict(updated_label_dict)

    response = await todoist_api_async.update_label(label_id=default_label.id, **args)

    assert len(requests_mock.calls) == 2
    assert response == Label.from_dict(updated_label_dict)


@pytest.mark.asyncio
async def test_delete_label(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
) -> None:
    label_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/labels/{label_id}"

    requests_mock.add(
        method="DELETE",
        url=endpoint,
        status=204,
    )

    response = todoist_api.delete_label(label_id)

    assert len(requests_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.delete_label(label_id)

    assert len(requests_mock.calls) == 2
    assert response is True
