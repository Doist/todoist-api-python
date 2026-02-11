from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from tests.data.test_defaults import DEFAULT_API_URL
from tests.utils.test_utils import (
    auth_matcher,
    data_matcher,
    mock_route,
    request_id_matcher,
)

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
        status=204,
        params={"name": name},
        matchers=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher({"new_name": new_name}),
        ],
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
        status=204,
        matchers=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher({"name": name}),
        ],
    )

    result = todoist_api.remove_shared_label(name)

    assert len(respx_mock.calls) == 1
    assert result is True

    result = await todoist_api_async.remove_shared_label(name)

    assert len(respx_mock.calls) == 2
    assert result is True
