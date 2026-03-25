from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from tests.data.test_defaults import (
    DEFAULT_API_URL,
    PaginatedResults,
)
from tests.utils.test_utils import api_headers, enumerate_async, mock_route
from todoist_api_python.models import LocationReminder

if TYPE_CHECKING:
    import respx

    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync


@pytest.mark.asyncio
async def test_get_location_reminder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_location_reminder_response: dict[str, Any],
    default_location_reminder: LocationReminder,
) -> None:
    location_reminder_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/location_reminders/{location_reminder_id}"

    mock_route(
        respx_mock,
        method="GET",
        url=endpoint,
        request_headers=api_headers(),
        response_json=default_location_reminder_response,
        response_status=200,
    )

    reminder = todoist_api.get_location_reminder(location_reminder_id)

    assert len(respx_mock.calls) == 1
    assert reminder == default_location_reminder

    reminder = await todoist_api_async.get_location_reminder(location_reminder_id)

    assert len(respx_mock.calls) == 2
    assert reminder == default_location_reminder


@pytest.mark.asyncio
async def test_get_location_reminders(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_location_reminders_response: list[PaginatedResults],
    default_location_reminders_list: list[list[LocationReminder]],
) -> None:
    task_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/location_reminders"

    cursor: str | None = None
    for page in default_location_reminders_response:
        mock_route(
            respx_mock,
            method="GET",
            url=endpoint,
            request_params={"task_id": task_id}
            | ({"cursor": cursor} if cursor else {}),
            request_headers=api_headers(),
            response_json=page,
            response_status=200,
        )
        cursor = page["next_cursor"]

    count = 0

    reminders_iter = todoist_api.get_location_reminders(task_id=task_id)

    for i, reminders in enumerate(reminders_iter):
        assert len(respx_mock.calls) == count + 1
        assert reminders == default_location_reminders_list[i]
        count += 1

    reminders_async_iter = await todoist_api_async.get_location_reminders(
        task_id=task_id
    )

    async for i, reminders in enumerate_async(reminders_async_iter):
        assert len(respx_mock.calls) == count + 1
        assert reminders == default_location_reminders_list[i]
        count += 1


@pytest.mark.asyncio
async def test_add_location_reminder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_location_reminder_response: dict[str, Any],
    default_location_reminder: LocationReminder,
) -> None:
    task_id = "6X7rM8997g3RQmvh"

    mock_route(
        respx_mock,
        method="POST",
        url=f"{DEFAULT_API_URL}/location_reminders",
        request_headers=api_headers(),
        request_json={
            "task_id": task_id,
            "name": "Office",
            "loc_lat": "51.5074",
            "loc_long": "-0.1278",
            "loc_trigger": "on_enter",
            "radius": 200,
        },
        response_json=default_location_reminder_response,
        response_status=200,
    )

    new_reminder = todoist_api.add_location_reminder(
        task_id=task_id,
        name="Office",
        loc_lat="51.5074",
        loc_long="-0.1278",
        loc_trigger="on_enter",
        radius=200,
    )

    assert len(respx_mock.calls) == 1
    assert new_reminder == default_location_reminder

    new_reminder = await todoist_api_async.add_location_reminder(
        task_id=task_id,
        name="Office",
        loc_lat="51.5074",
        loc_long="-0.1278",
        loc_trigger="on_enter",
        radius=200,
    )

    assert len(respx_mock.calls) == 2
    assert new_reminder == default_location_reminder


@pytest.mark.asyncio
async def test_update_location_reminder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_location_reminder: LocationReminder,
) -> None:
    args = {
        "name": "Home Office",
        "radius": 150,
    }
    updated_dict = default_location_reminder.to_dict() | args

    mock_route(
        respx_mock,
        method="POST",
        url=f"{DEFAULT_API_URL}/location_reminders/{default_location_reminder.id}",
        request_headers=api_headers(),
        request_json=args,
        response_json=updated_dict,
        response_status=200,
    )

    response = todoist_api.update_location_reminder(
        location_reminder_id=default_location_reminder.id, **args
    )

    assert len(respx_mock.calls) == 1
    assert response == LocationReminder.from_dict(updated_dict)

    response = await todoist_api_async.update_location_reminder(
        location_reminder_id=default_location_reminder.id, **args
    )

    assert len(respx_mock.calls) == 2
    assert response == LocationReminder.from_dict(updated_dict)


@pytest.mark.asyncio
async def test_delete_location_reminder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
) -> None:
    location_reminder_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/location_reminders/{location_reminder_id}"

    mock_route(
        respx_mock,
        method="DELETE",
        url=endpoint,
        request_headers=api_headers(),
        response_status=204,
    )

    response = todoist_api.delete_location_reminder(location_reminder_id)

    assert len(respx_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.delete_location_reminder(location_reminder_id)

    assert len(respx_mock.calls) == 2
    assert response is True
