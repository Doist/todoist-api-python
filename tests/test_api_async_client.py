from __future__ import annotations

import asyncio
import warnings

from tests.data.test_defaults import DEFAULT_TOKEN
from todoist_api_python.api_async import TodoistAPIAsync


def test_warns_if_async_client_is_not_closed() -> None:
    api = TodoistAPIAsync(DEFAULT_TOKEN)

    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always", ResourceWarning)
        api.__del__()

    assert any(item.category is ResourceWarning for item in caught)

    asyncio.run(api.close())
