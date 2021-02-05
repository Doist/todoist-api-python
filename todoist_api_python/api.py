from typing import Any, Dict, List

import requests

from todoist_api_python.endpoints import (
    COLLABORATORS_ENDPOINT,
    COMMENTS_ENDPOINT,
    LABELS_ENDPOINT,
    PROJECTS_ENDPOINT,
    SECTIONS_ENDPOINT,
    TASKS_ENDPOINT,
    get_rest_url,
)
from todoist_api_python.http_requests import delete, get, post
from todoist_api_python.models import (
    Collaborator,
    Comment,
    Label,
    Project,
    Section,
    Task,
)


class TodoistAPI:
    def __init__(self, token: str, session=None):
        self._token: str = token
        self._session = session or requests.Session()

    def get_task(self, task_id: int) -> Task:
        endpoint = get_rest_url(f"{TASKS_ENDPOINT}/{task_id}")
        task = get(self._session, self._token, endpoint)
        return Task.from_dict(task)

    def get_tasks(self, **kwargs) -> List[Task]:
        ids = kwargs.pop("ids", None)

        if ids:
            kwargs.update({"ids": ",".join(str(i) for i in ids)})

        endpoint = get_rest_url(TASKS_ENDPOINT)
        tasks = get(self._session, self._token, endpoint, kwargs)
        return [Task.from_dict(obj) for obj in tasks]

    def add_task(self, content: str, **kwargs) -> Task:
        endpoint = get_rest_url(TASKS_ENDPOINT)
        data: Dict[str, Any] = {"content": content}
        data.update(kwargs)
        task = post(self._session, self._token, endpoint, data=data)
        return Task.from_dict(task)

    def update_task(self, task_id: int, **kwargs) -> bool:
        endpoint = get_rest_url(f"{TASKS_ENDPOINT}/{task_id}")
        success = post(self._session, self._token, endpoint, data=kwargs)
        return success

    def close_task(self, task_id: int, **kwargs) -> bool:
        endpoint = get_rest_url(f"{TASKS_ENDPOINT}/{task_id}/close")
        success = post(self._session, self._token, endpoint, data=kwargs)
        return success

    def reopen_task(self, task_id: int, **kwargs) -> bool:
        endpoint = get_rest_url(f"{TASKS_ENDPOINT}/{task_id}/reopen")
        success = post(self._session, self._token, endpoint, data=kwargs)
        return success

    def delete_task(self, task_id: int, **kwargs) -> bool:
        endpoint = get_rest_url(f"{TASKS_ENDPOINT}/{task_id}")
        success = delete(self._session, self._token, endpoint, args=kwargs)
        return success

    def get_project(self, project_id: int) -> Project:
        endpoint = get_rest_url(f"{PROJECTS_ENDPOINT}/{project_id}")
        project = get(self._session, self._token, endpoint)
        return Project.from_dict(project)

    def get_projects(self) -> List[Project]:
        endpoint = get_rest_url(PROJECTS_ENDPOINT)
        projects = get(self._session, self._token, endpoint)
        return [Project.from_dict(obj) for obj in projects]

    def add_project(self, name: str, **kwargs) -> Project:
        endpoint = get_rest_url(PROJECTS_ENDPOINT)
        data: Dict[str, Any] = {"name": name}
        data.update(kwargs)
        project = post(self._session, self._token, endpoint, data=data)
        return Project.from_dict(project)

    def update_project(self, project_id: int, **kwargs) -> bool:
        endpoint = get_rest_url(f"{PROJECTS_ENDPOINT}/{project_id}")
        success = post(self._session, self._token, endpoint, data=kwargs)
        return success

    def delete_project(self, project_id: int, **kwargs) -> bool:
        endpoint = get_rest_url(f"{PROJECTS_ENDPOINT}/{project_id}")
        success = delete(self._session, self._token, endpoint, args=kwargs)
        return success

    def get_collaborators(self, project_id: int) -> List[Collaborator]:
        endpoint = get_rest_url(
            f"{PROJECTS_ENDPOINT}/{project_id}/{COLLABORATORS_ENDPOINT}"
        )
        collaborators = get(self._session, self._token, endpoint)
        return [Collaborator.from_dict(obj) for obj in collaborators]

    def get_section(self, section_id: int) -> Section:
        endpoint = get_rest_url(f"{SECTIONS_ENDPOINT}/{section_id}")
        section = get(self._session, self._token, endpoint)
        return Section.from_dict(section)

    def get_sections(self, **kwargs) -> List[Section]:
        endpoint = get_rest_url(SECTIONS_ENDPOINT)
        sections = get(self._session, self._token, endpoint, kwargs)
        return [Section.from_dict(obj) for obj in sections]

    def add_section(self, name: str, project_id: int, **kwargs) -> Section:
        endpoint = get_rest_url(SECTIONS_ENDPOINT)
        data = {"name": name, "project_id": project_id}
        data.update(kwargs)
        section = post(self._session, self._token, endpoint, data=data)
        return Section.from_dict(section)

    def update_section(self, section_id: int, name: str, **kwargs) -> bool:
        endpoint = get_rest_url(f"{SECTIONS_ENDPOINT}/{section_id}")
        data: Dict[str, Any] = {"name": name}
        data.update(kwargs)
        success = post(self._session, self._token, endpoint, data=data)
        return success

    def delete_section(self, section_id: int, **kwargs) -> bool:
        endpoint = get_rest_url(f"{SECTIONS_ENDPOINT}/{section_id}")
        success = delete(self._session, self._token, endpoint, args=kwargs)
        return success

    def get_comment(self, comment_id: int) -> Comment:
        endpoint = get_rest_url(f"{COMMENTS_ENDPOINT}/{comment_id}")
        comment = get(self._session, self._token, endpoint)
        return Comment.from_dict(comment)

    def get_comments(self, **kwargs) -> List[Comment]:
        endpoint = get_rest_url(COMMENTS_ENDPOINT)
        comments = get(self._session, self._token, endpoint, kwargs)
        return [Comment.from_dict(obj) for obj in comments]

    def add_comment(self, content: str, **kwargs) -> Comment:
        endpoint = get_rest_url(COMMENTS_ENDPOINT)
        data = {"content": content}
        data.update(kwargs)
        comment = post(self._session, self._token, endpoint, data=data)
        return Comment.from_dict(comment)

    def update_comment(self, comment_id: int, content: str, **kwargs) -> bool:
        endpoint = get_rest_url(f"{COMMENTS_ENDPOINT}/{comment_id}")
        data: Dict[str, Any] = {"content": content}
        data.update(kwargs)
        success = post(self._session, self._token, endpoint, data=data)
        return success

    def delete_comment(self, comment_id: int, **kwargs) -> bool:
        endpoint = get_rest_url(f"{COMMENTS_ENDPOINT}/{comment_id}")
        success = delete(self._session, self._token, endpoint, args=kwargs)
        return success

    def get_label(self, label_id: int) -> Label:
        endpoint = get_rest_url(f"{LABELS_ENDPOINT}/{label_id}")
        label = get(self._session, self._token, endpoint)
        return Label.from_dict(label)

    def get_labels(self) -> List[Label]:
        endpoint = get_rest_url(LABELS_ENDPOINT)
        labels = get(self._session, self._token, endpoint)
        return [Label.from_dict(obj) for obj in labels]

    def add_label(self, name: str, **kwargs) -> Label:
        endpoint = get_rest_url(LABELS_ENDPOINT)
        data = {"name": name}
        data.update(kwargs)
        label = post(self._session, self._token, endpoint, data=data)
        return Label.from_dict(label)

    def update_label(self, label_id: int, **kwargs) -> bool:
        endpoint = get_rest_url(f"{LABELS_ENDPOINT}/{label_id}")
        success = post(self._session, self._token, endpoint, data=kwargs)
        return success

    def delete_label(self, label_id: int, **kwargs) -> bool:
        endpoint = get_rest_url(f"{LABELS_ENDPOINT}/{label_id}")
        success = delete(self._session, self._token, endpoint, args=kwargs)
        return success
