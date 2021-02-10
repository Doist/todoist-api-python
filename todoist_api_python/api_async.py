from typing import List

from todoist_api_python.api import TodoistAPI
from todoist_api_python.models import (
    Collaborator,
    Comment,
    Label,
    Project,
    QuickAddResult,
    Section,
    Task,
)
from todoist_api_python.utils import run_async


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

    async def quick_add_task(self, text: str) -> QuickAddResult:
        return await run_async(lambda: self._api.quick_add_task(text))

    async def get_project(self, project_id: int) -> Project:
        return await run_async(lambda: self._api.get_project(project_id))

    async def get_projects(self) -> List[Project]:
        return await run_async(lambda: self._api.get_projects())

    async def add_project(self, name: str, **kwargs) -> Project:
        return await run_async(lambda: self._api.add_project(name, **kwargs))

    async def update_project(self, project_id: int, **kwargs) -> bool:
        return await run_async(lambda: self._api.update_project(project_id, **kwargs))

    async def delete_project(self, project_id: int, **kwargs) -> bool:
        return await run_async(lambda: self._api.delete_project(project_id, **kwargs))

    async def get_collaborators(self, project_id: int) -> List[Collaborator]:
        return await run_async(lambda: self._api.get_collaborators(project_id))

    async def get_section(self, section_id: int) -> Section:
        return await run_async(lambda: self._api.get_section(section_id))

    async def get_sections(self, **kwargs) -> List[Section]:
        return await run_async(lambda: self._api.get_sections(**kwargs))

    async def add_section(self, name: str, project_id: int, **kwargs) -> Section:
        return await run_async(
            lambda: self._api.add_section(name, project_id, **kwargs)
        )

    async def update_section(self, section_id: int, name: str, **kwargs) -> bool:
        return await run_async(
            lambda: self._api.update_section(section_id, name, **kwargs)
        )

    async def delete_section(self, section_id: int, **kwargs) -> bool:
        return await run_async(lambda: self._api.delete_section(section_id, **kwargs))

    async def get_comment(self, comment_id: int) -> Comment:
        return await run_async(lambda: self._api.get_comment(comment_id))

    async def get_comments(self, **kwargs) -> List[Comment]:
        return await run_async(lambda: self._api.get_comments(**kwargs))

    async def add_comment(self, content: str, **kwargs) -> Comment:
        return await run_async(lambda: self._api.add_comment(content, **kwargs))

    async def update_comment(self, comment_id: int, content: str, **kwargs) -> bool:
        return await run_async(
            lambda: self._api.update_comment(comment_id, content, **kwargs)
        )

    async def delete_comment(self, comment_id: int, **kwargs) -> bool:
        return await run_async(lambda: self._api.delete_comment(comment_id, **kwargs))

    async def get_label(self, label_id: int) -> Label:
        return await run_async(lambda: self._api.get_label(label_id))

    async def get_labels(self) -> List[Label]:
        return await run_async(lambda: self._api.get_labels())

    async def add_label(self, name: str, **kwargs) -> Label:
        return await run_async(lambda: self._api.add_label(name, **kwargs))

    async def update_label(self, label_id: int, **kwargs) -> bool:
        return await run_async(lambda: self._api.update_label(label_id, **kwargs))

    async def delete_label(self, label_id: int, **kwargs) -> bool:
        return await run_async(lambda: self._api.delete_label(label_id, **kwargs))
