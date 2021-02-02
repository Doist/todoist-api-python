import asyncio
from typing import List

from todoist_api_python import TodoistAPI
from todoist_api_python.models import Task


async def run_async(func):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func)


class TodoistAPIAsync:
    def __init__(self, token: str):
        self._api = TodoistAPI(token)

    async def get_task(self, task_id: int) -> Task:
        return await run_async(lambda: self._api.get_task(task_id))

    async def get_tasks(self, **kwargs) -> List[Task]:
        return await run_async(lambda: self._api.get_tasks(**kwargs))

    async def add_task(self, content: str, **kwargs) -> Task:
        return await run_async(lambda: self._api.add_task(content, **kwargs))

    async def update_task(self, task_id: int, **kwargs) -> bool:
        return await run_async(lambda: self._api.update_task(task_id, **kwargs))

    async def close_task(self, task_id: int, **kwargs) -> bool:
        return await run_async(lambda: self._api.close_task(task_id, **kwargs))

    async def reopen_task(self, task_id: int, **kwargs) -> bool:
        return await run_async(lambda: self._api.reopen_task(task_id, **kwargs))

    async def delete_task(self, task_id: int, **kwargs) -> bool:
        return await run_async(lambda: self._api.delete_task(task_id, **kwargs))
