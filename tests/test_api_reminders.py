from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from tests.data.test_defaults import (
    DEFAULT_API_URL,
    DEFAULT_DUE_RESPONSE,
    PaginatedResults,
)
from tests.utils.test_utils import api_headers, enumerate_async, mock_route
from todoist_api_python.models import Due, Reminder

if TYPE_CHECKING:
    import respx

    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync


@pytest.mark.asyncio
async def test_get_reminder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_reminder_response: dict[str, Any],
    default_reminder: Reminder,
) -> None:
    reminder_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/reminders/{reminder_id}"

    mock_route(
        respx_mock,
        method="GET",
        url=endpoint,
        request_headers=api_headers(),
        response_json=default_reminder_response,
        response_status=200,
    )

    reminder = todoist_api.get_reminder(reminder_id)

    assert len(respx_mock.calls) == 1
    assert reminder == default_reminder

    reminder = await todoist_api_async.get_reminder(reminder_id)

    assert len(respx_mock.calls) == 2
    assert reminder == default_reminder


@pytest.mark.asyncio
async def test_get_reminders(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_reminders_response: list[PaginatedResults],
    default_reminders_list: list[list[Reminder]],
) -> None:
    task_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/reminders"

    cursor: str | None = None
    for page in default_reminders_response:
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

    reminders_iter = todoist_api.get_reminders(task_id=task_id)

    for i, reminders in enumerate(reminders_iter):
        assert len(respx_mock.calls) == count + 1
        assert reminders == default_reminders_list[i]
        count += 1

    reminders_async_iter = await todoist_api_async.get_reminders(task_id=task_id)

    async for i, reminders in enumerate_async(reminders_async_iter):
        assert len(respx_mock.calls) == count + 1
        assert reminders == default_reminders_list[i]
        count += 1


@pytest.mark.asyncio
async def test_add_reminder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_reminder_response: dict[str, Any],
    default_reminder: Reminder,
) -> None:
    task_id = "6X7rM8997g3RQmvh"
    due = Due.from_dict(DEFAULT_DUE_RESPONSE)

    mock_route(
        respx_mock,
        method="POST",
        url=f"{DEFAULT_API_URL}/reminders",
        request_headers=api_headers(),
        request_json={
            "task_id": task_id,
            "reminder_type": "absolute",
            "due": due.to_dict(),
            "service": "push",
        },
        response_json=default_reminder_response,
        response_status=200,
    )

    new_reminder = todoist_api.add_reminder(
        task_id=task_id,
        reminder_type="absolute",
        due=due,
        service="push",
    )

    assert len(respx_mock.calls) == 1
    assert new_reminder == default_reminder

    new_reminder = await todoist_api_async.add_reminder(
        task_id=task_id,
        reminder_type="absolute",
        due=due,
        service="push",
    )

    assert len(respx_mock.calls) == 2
    assert new_reminder == default_reminder


@pytest.mark.asyncio
async def test_update_reminder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
    default_reminder: Reminder,
) -> None:
    args = {
        "minute_offset": 45,
    }
    updated_reminder_dict = default_reminder.to_dict() | args

    mock_route(
        respx_mock,
        method="POST",
        url=f"{DEFAULT_API_URL}/reminders/{default_reminder.id}",
        request_headers=api_headers(),
        request_json=args,
        response_json=updated_reminder_dict,
        response_status=200,
    )

    response = todoist_api.update_reminder(reminder_id=default_reminder.id, **args)

    assert len(respx_mock.calls) == 1
    assert response == Reminder.from_dict(updated_reminder_dict)

    response = await todoist_api_async.update_reminder(
        reminder_id=default_reminder.id, **args
    )

    assert len(respx_mock.calls) == 2
    assert response == Reminder.from_dict(updated_reminder_dict)


@pytest.mark.asyncio
async def test_delete_reminder(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
) -> None:
    reminder_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/reminders/{reminder_id}"

    mock_route(
        respx_mock,
        method="DELETE",
        url=endpoint,
        request_headers=api_headers(),
        response_status=204,
    )

    response = todoist_api.delete_reminder(reminder_id)

    assert len(respx_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.delete_reminder(reminder_id)

    assert len(respx_mock.calls) == 2
    assert response is True
