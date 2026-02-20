from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.data.test_defaults import DEFAULT_API_URL
from tests.utils.test_utils import api_headers, mock_route

if TYPE_CHECKING:
    import respx

    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync


@pytest.mark.asyncio
async def test_rename_shared_label(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
) -> None:
    name = "old-shared-label"
    new_name = "new-shared-label"
    endpoint = f"{DEFAULT_API_URL}/labels/shared/rename"

    mock_route(
        respx_mock,
        method="POST",
        url=endpoint,
        request_params={"name": name},
        request_headers=api_headers(),
        request_json={"new_name": new_name},
        response_status=204,
    )

    result = todoist_api.rename_shared_label(name, new_name)

    assert len(respx_mock.calls) == 1
    assert result is True

    result = await todoist_api_async.rename_shared_label(name, new_name)

    assert len(respx_mock.calls) == 2
    assert result is True


@pytest.mark.asyncio
async def test_remove_shared_label(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    respx_mock: respx.MockRouter,
) -> None:
    name = "Shared Label"
    endpoint = f"{DEFAULT_API_URL}/labels/shared/remove"

    mock_route(
        respx_mock,
        method="POST",
        url=endpoint,
        request_headers=api_headers(),
        request_json={"name": name},
        response_status=204,
    )

    result = todoist_api.remove_shared_label(name)

    assert len(respx_mock.calls) == 1
    assert result is True

    result = await todoist_api_async.remove_shared_label(name)

    assert len(respx_mock.calls) == 2
    assert result is True
