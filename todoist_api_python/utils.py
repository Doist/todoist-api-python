from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING, TypeVar

if TYPE_CHECKING:
    from collections.abc import Callable

SHOW_TASK_ENDPOINT = "https://todoist.com/showTask"


def get_url_for_task(task_id: int, sync_id: int | None) -> str:
    return (
        f"{SHOW_TASK_ENDPOINT}?id={task_id}&sync_id={sync_id}"
        if sync_id
        else f"{SHOW_TASK_ENDPOINT}?id={task_id}"
    )


T = TypeVar("T")


async def run_async(func: Callable[[], T]) -> T:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func)
