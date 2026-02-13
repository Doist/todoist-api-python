from __future__ import annotations

import sys
import warnings
from collections.abc import AsyncIterator, Callable
from typing import TYPE_CHECKING, Annotated, Any, Literal, TypeVar

import httpx
from annotated_types import Ge, Le, MaxLen, MinLen

from todoist_api_python._core.endpoints import (
    COLLABORATORS_PATH,
    COMMENTS_PATH,
    LABELS_PATH,
    LABELS_SEARCH_PATH_SUFFIX,
    PROJECT_ARCHIVE_PATH_SUFFIX,
    PROJECT_UNARCHIVE_PATH_SUFFIX,
    PROJECTS_PATH,
    PROJECTS_SEARCH_PATH_SUFFIX,
    SECTIONS_PATH,
    SECTIONS_SEARCH_PATH_SUFFIX,
    SHARED_LABELS_PATH,
    SHARED_LABELS_REMOVE_PATH,
    SHARED_LABELS_RENAME_PATH,
    TASKS_COMPLETED_BY_COMPLETION_DATE_PATH,
    TASKS_COMPLETED_BY_DUE_DATE_PATH,
    TASKS_FILTER_PATH,
    TASKS_PATH,
    TASKS_QUICK_ADD_PATH,
    get_api_url,
)
from todoist_api_python._core.http_requests import (
    delete_async,
    get_async,
    post_async,
)
from todoist_api_python._core.utils import (
    default_request_id_fn,
    format_date,
    format_datetime,
    kwargs_without_none,
)
from todoist_api_python.models import (
    Attachment,
    Collaborator,
    Comment,
    Label,
    Project,
    Section,
    Task,
)

if TYPE_CHECKING:
    from datetime import date, datetime
    from types import TracebackType

    from todoist_api_python.types import ColorString, LanguageCode, ViewStyle

if sys.version_info >= (3, 11):
    from typing import Self
else:
    Self = TypeVar("Self", bound="TodoistAPIAsync")


class TodoistAPIAsync:
    """
    Async client for the Todoist API.

    Provides asynchronous methods for interacting with Todoist resources like
    tasks, projects, labels, comments, etc.

    Manages an HTTP client and handles authentication.

    Prefer using this class as an async context manager to ensure the underlying
    `httpx.AsyncClient` is always closed. If you do not use `async with`, call
    `await close()` explicitly.
    """

    def __init__(
        self,
        token: str,
        request_id_fn: Callable[[], str] | None = default_request_id_fn,
        client: httpx.AsyncClient | None = None,
    ) -> None:
        """
        Initialize the TodoistAPIAsync client.

        :param token: Authentication token for the Todoist API.
        :param request_id_fn: Generator of request IDs for the `X-Request-ID` header.
        :param client: An optional pre-configured `httpx.AsyncClient` object, to be
            fully managed by `TodoistAPIAsync`.
        """
        self._token = token
        self._request_id_fn = request_id_fn
        self._client = client or httpx.AsyncClient()

    async def __aenter__(self) -> Self:
        """
        Enters the runtime context related to this object.

        The with statement will bind this method's return value to the target(s)
        specified in the as clause of the statement, if any.

        :return: This TodoistAPIAsync instance.
        """
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the async runtime context and close the underlying httpx client."""
        await self.close()

    async def close(self) -> None:
        """Close the underlying `httpx.AsyncClient`."""
        await self._client.aclose()

    def __del__(self) -> None:
        """Warn when the async client was not explicitly closed."""
        client = getattr(self, "_client", None)
        if client is None or client.is_closed:
            return

        warnings.warn(
            "TodoistAPIAsync client was not closed. "
            "Use `async with TodoistAPIAsync(...)` or call `await api.close()`.",
            ResourceWarning,
            stacklevel=2,
        )

    async def get_task(self, task_id: str) -> Task:
        """
        Get a specific task by its ID.

        :param task_id: The ID of the task to retrieve.
        :return: The requested task.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Task dictionary.
        """
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}")
        task_data: dict[str, Any] = await get_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )
        return Task.from_dict(task_data)

    async def get_tasks(
        self,
        *,
        project_id: str | None = None,
        section_id: str | None = None,
        parent_id: str | None = None,
        label: str | None = None,
        ids: list[str] | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Task]]:
        """
        Get an iterable of lists of active tasks.

        The response is an iterable of lists of active tasks matching the criteria.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param project_id: Filter tasks by project ID.
        :param section_id: Filter tasks by section ID.
        :param parent_id: Filter tasks by parent task ID.
        :param label: Filter tasks by label name.
        :param ids: A list of the IDs of the tasks to retrieve.
        :param limit: Maximum number of tasks per page.
        :return: An iterable of lists of tasks.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(TASKS_PATH)

        params = kwargs_without_none(
            project_id=project_id,
            section_id=section_id,
            parent_id=parent_id,
            label=label,
            ids=",".join(str(i) for i in ids) if ids is not None else None,
            limit=limit,
        )

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            Task.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def filter_tasks(
        self,
        *,
        query: Annotated[str, MaxLen(1024)] | None = None,
        lang: str | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Task]]:
        """
        Get an iterable of lists of active tasks matching the filter.

        The response is an iterable of lists of active tasks matching the criteria.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param query: Query tasks using Todoist's filter language.
        :param lang: Language for task content (e.g., 'en').
        :param limit: Maximum number of tasks per page.
        :return: An iterable of lists of tasks.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(TASKS_FILTER_PATH)

        params = kwargs_without_none(query=query, lang=lang, limit=limit)

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            Task.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def add_task(
        self,
        content: Annotated[str, MinLen(1), MaxLen(500)],
        *,
        description: Annotated[str, MaxLen(16383)] | None = None,
        project_id: str | None = None,
        section_id: str | None = None,
        parent_id: str | None = None,
        labels: list[Annotated[str, MaxLen(100)]] | None = None,
        priority: Annotated[int, Ge(1), Le(4)] | None = None,
        due_string: Annotated[str, MaxLen(150)] | None = None,
        due_lang: LanguageCode | None = None,
        due_date: date | None = None,
        due_datetime: datetime | None = None,
        assignee_id: str | None = None,
        order: int | None = None,
        auto_reminder: bool | None = None,
        auto_parse_labels: bool | None = None,
        duration: Annotated[int, Ge(1)] | None = None,
        duration_unit: Literal["minute", "day"] | None = None,
        deadline_date: date | None = None,
        deadline_lang: LanguageCode | None = None,
    ) -> Task:
        """
        Create a new task.

        :param content: The text content of the task.
        :param project_id: The ID of the project to add the task to.
        :param section_id: The ID of the section to add the task to.
        :param parent_id: The ID of the parent task.
        :param labels: The task's labels (a list of names).
        :param priority: The priority of the task (4 for very urgent).
        :param due_string: The due date in natural language format.
        :param due_lang: Language for parsing the due date (e.g., 'en').
        :param due_date: The due date as a date object.
        :param due_datetime: The due date and time as a datetime object.
        :param assignee_id: User ID to whom the task is assigned.
        :param description: Description for the task.
        :param order: The order of task in the project or section.
        :param auto_reminder: Whether to add default reminder if date with time is set.
        :param auto_parse_labels: Whether to parse labels from task content.
        :param duration: The amount of time the task will take.
        :param duration_unit: The unit of time for duration.
        :param deadline_date: The deadline date as a date object.
        :param deadline_lang: Language for parsing the deadline date.
        :return: The newly created task.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Task dictionary.
        """
        endpoint = get_api_url(TASKS_PATH)

        data = kwargs_without_none(
            content=content,
            description=description,
            project_id=project_id,
            section_id=section_id,
            parent_id=parent_id,
            labels=labels,
            priority=priority,
            due_string=due_string,
            due_lang=due_lang,
            due_date=format_date(due_date) if due_date is not None else None,
            due_datetime=(
                format_datetime(due_datetime) if due_datetime is not None else None
            ),
            assignee_id=assignee_id,
            order=order,
            auto_reminder=auto_reminder,
            auto_parse_labels=auto_parse_labels,
            duration=duration,
            duration_unit=duration_unit,
            deadline_date=(
                format_date(deadline_date) if deadline_date is not None else None
            ),
            deadline_lang=deadline_lang,
        )

        task_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )
        return Task.from_dict(task_data)

    async def add_task_quick(
        self,
        text: str,
        *,
        note: str | None = None,
        reminder: str | None = None,
        auto_reminder: bool = True,
    ) -> Task:
        """
        Create a new task using Todoist's Quick Add syntax.

        This automatically parses dates, deadlines, projects, labels, priorities, etc,
        from the provided text (e.g., "Buy milk #Shopping @groceries tomorrow p1").

        :param text: The task text using Quick Add syntax.
        :param note: Optional note to be added to the task.
        :param reminder: Optional reminder date in free form text.
        :param auto_reminder: Whether to add default reminder if date with time is set.
        :return: A result object containing the parsed task data and metadata.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response cannot be parsed into a QuickAddResult.
        """
        endpoint = get_api_url(TASKS_QUICK_ADD_PATH)

        data = kwargs_without_none(
            meta=True,
            text=text,
            auto_reminder=auto_reminder,
            note=note,
            reminder=reminder,
        )

        task_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )
        return Task.from_dict(task_data)

    async def update_task(
        self,
        task_id: str,
        *,
        content: Annotated[str, MinLen(1), MaxLen(500)] | None = None,
        description: Annotated[str, MaxLen(16383)] | None = None,
        labels: list[Annotated[str, MaxLen(60)]] | None = None,
        priority: Annotated[int, Ge(1), Le(4)] | None = None,
        due_string: Annotated[str, MaxLen(150)] | None = None,
        due_lang: LanguageCode | None = None,
        due_date: date | None = None,
        due_datetime: datetime | None = None,
        assignee_id: str | None = None,
        day_order: int | None = None,
        collapsed: bool | None = None,
        duration: Annotated[int, Ge(1)] | None = None,
        duration_unit: Literal["minute", "day"] | None = None,
        deadline_date: date | None = None,
        deadline_lang: LanguageCode | None = None,
    ) -> Task:
        """
        Update an existing task.

        Only the fields to be updated need to be provided.

        :param task_id: The ID of the task to update.
        :param content: The text content of the task.
        :param description: Description for the task.
        :param labels: The task's labels (a list of names).
        :param priority: The priority of the task (4 for very urgent).
        :param due_string: The due date in natural language format.
        :param due_lang: Language for parsing the due date (e.g., 'en').
        :param due_date: The due date as a date object.
        :param due_datetime: The due date and time as a datetime object.
        :param assignee_id: User ID to whom the task is assigned.
        :param day_order: The order of the task inside Today or Next 7 days view.
        :param collapsed: Whether the task's sub-tasks are collapsed.
        :param duration: The amount of time the task will take.
        :param duration_unit: The unit of time for duration.
        :param deadline_date: The deadline date as a date object.
        :param deadline_lang: Language for parsing the deadline date.
        :return: the updated Task.
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}")

        data = kwargs_without_none(
            content=content,
            description=description,
            labels=labels,
            priority=priority,
            due_string=due_string,
            due_lang=due_lang,
            due_date=format_date(due_date) if due_date is not None else None,
            due_datetime=(
                format_datetime(due_datetime) if due_datetime is not None else None
            ),
            assignee_id=assignee_id,
            day_order=day_order,
            collapsed=collapsed,
            duration=duration,
            duration_unit=duration_unit,
            deadline_date=(
                format_date(deadline_date) if deadline_date is not None else None
            ),
            deadline_lang=deadline_lang,
        )

        task_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )
        return Task.from_dict(task_data)

    async def complete_task(self, task_id: str) -> bool:
        """
        Complete a task.

        For recurring tasks, this schedules the next occurrence.
        For non-recurring tasks, it marks them as completed.

        :param task_id: The ID of the task to close.
        :return: True if the task was closed successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}/close")
        return await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )

    async def uncomplete_task(self, task_id: str) -> bool:
        """
        Uncomplete a (completed) task.

        Any parent tasks or sections will also be uncompleted.

        :param task_id: The ID of the task to reopen.
        :return: True if the task was uncompleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}/reopen")
        return await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )

    async def move_task(
        self,
        task_id: str,
        project_id: str | None = None,
        section_id: str | None = None,
        parent_id: str | None = None,
    ) -> bool:
        """
        Move a task to a different project, section, or parent task.

        `project_id` takes predence, followed by
        `section_id` (which also updates `project_id`),
        and then `parent_id` (which also updates `section_id` and `project_id`).

        :param task_id: The ID of the task to move.
        :param project_id: The ID of the project to move the task to.
        :param section_id: The ID of the section to move the task to.
        :param parent_id: The ID of the parent to move the task to.
        :return: True if the task was moved successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises ValueError: If neither `project_id`, `section_id`,
                nor `parent_id` is provided.
        """
        if project_id is None and section_id is None and parent_id is None:
            raise ValueError(
                "Either `project_id`, `section_id`, or `parent_id` must be provided."
            )

        data = kwargs_without_none(
            project_id=project_id,
            section_id=section_id,
            parent_id=parent_id,
        )
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}/move")
        return await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )

    async def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        :param task_id: The ID of the task to delete.
        :return: True if the task was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}")
        return await delete_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )

    async def get_completed_tasks_by_due_date(
        self,
        *,
        since: datetime,
        until: datetime,
        workspace_id: str | None = None,
        project_id: str | None = None,
        section_id: str | None = None,
        parent_id: str | None = None,
        filter_query: str | None = None,
        filter_lang: str | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Task]]:
        """
        Get an iterable of lists of completed tasks within a due date range.

        Retrieves tasks completed within a specific due date range (up to 6 weeks).
        Supports filtering by workspace, project, section, parent task, or a query.

        The response is an iterable of lists of completed tasks. Be aware that each
        iteration fires off a network request to the Todoist API, and may result in
        rate limiting or other API restrictions.

        :param since: Start of the date range (inclusive).
        :param until: End of the date range (inclusive).
        :param workspace_id: Filter by workspace ID.
        :param project_id: Filter by project ID.
        :param section_id: Filter by section ID.
        :param parent_id: Filter by parent task ID.
        :param filter_query: Filter by a query string.
        :param filter_lang: Language for the filter query (e.g., 'en').
        :param limit: Maximum number of tasks per page (default 50).
        :return: An iterable of lists of completed tasks.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(TASKS_COMPLETED_BY_DUE_DATE_PATH)

        params = kwargs_without_none(
            since=format_datetime(since),
            until=format_datetime(until),
            workspace_id=workspace_id,
            project_id=project_id,
            section_id=section_id,
            parent_id=parent_id,
            filter_query=filter_query,
            filter_lang=filter_lang,
            limit=limit,
        )

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "items",
            Task.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def get_completed_tasks_by_completion_date(
        self,
        *,
        since: datetime,
        until: datetime,
        workspace_id: str | None = None,
        filter_query: str | None = None,
        filter_lang: str | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Task]]:
        """
        Get an iterable of lists of completed tasks within a date range.

        Retrieves tasks completed within a specific date range (up to 3 months).
        Supports filtering by workspace or a filter query.

        The response is an iterable of lists of completed tasks. Be aware that each
        iteration fires off a network request to the Todoist API, and may result in
        rate limiting or other API restrictions.

        :param since: Start of the date range (inclusive).
        :param until: End of the date range (inclusive).
        :param workspace_id: Filter by workspace ID.
        :param filter_query: Filter by a query string.
        :param filter_lang: Language for the filter query (e.g., 'en').
        :param limit: Maximum number of tasks per page (default 50).
        :return: An iterable of lists of completed tasks.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(TASKS_COMPLETED_BY_COMPLETION_DATE_PATH)

        params = kwargs_without_none(
            since=format_datetime(since),
            until=format_datetime(until),
            workspace_id=workspace_id,
            filter_query=filter_query,
            filter_lang=filter_lang,
            limit=limit,
        )

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "items",
            Task.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def get_project(self, project_id: str) -> Project:
        """
        Get a project by its ID.

        :param project_id: The ID of the project to retrieve.
        :return: The requested project.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Project dictionary.
        """
        endpoint = get_api_url(f"{PROJECTS_PATH}/{project_id}")
        project_data: dict[str, Any] = await get_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )
        return Project.from_dict(project_data)

    async def get_projects(
        self,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Project]]:
        """
        Get an iterable of lists of active projects.

        The response is an iterable of lists of active projects.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param limit: Maximum number of projects per page.
        :return: An iterable of lists of projects.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(PROJECTS_PATH)
        params = kwargs_without_none(limit=limit)
        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            Project.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def search_projects(
        self,
        query: Annotated[str, MinLen(1), MaxLen(1024)],
        *,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Project]]:
        """
        Search active projects by name.

        The response is an iterable of lists of projects matching the query.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param query: Query string for project names.
        :param limit: Maximum number of projects per page.
        :return: An iterable of lists of projects.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(f"{PROJECTS_PATH}/{PROJECTS_SEARCH_PATH_SUFFIX}")

        params = kwargs_without_none(query=query, limit=limit)

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            Project.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def add_project(
        self,
        name: Annotated[str, MinLen(1), MaxLen(120)],
        *,
        description: Annotated[str, MaxLen(16383)] | None = None,
        parent_id: str | None = None,
        color: ColorString | None = None,
        is_favorite: bool | None = None,
        view_style: ViewStyle | None = None,
    ) -> Project:
        """
        Create a new project.

        :param name: The name of the project.
        :param description: Description for the project (up to 1024 characters).
        :param parent_id: The ID of the parent project. Set to null for root projects.
        :param color: The color of the project icon.
        :param is_favorite: Whether the project is a favorite.
        :param view_style: A string value (either 'list' or 'board', default is 'list').
        :return: The newly created project.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Project dictionary.
        """
        endpoint = get_api_url(PROJECTS_PATH)

        data = kwargs_without_none(
            name=name,
            parent_id=parent_id,
            description=description,
            color=color,
            is_favorite=is_favorite,
            view_style=view_style,
        )

        project_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )
        return Project.from_dict(project_data)

    async def update_project(
        self,
        project_id: str,
        *,
        name: Annotated[str, MinLen(1), MaxLen(120)] | None = None,
        description: Annotated[str, MaxLen(16383)] | None = None,
        color: ColorString | None = None,
        is_favorite: bool | None = None,
        view_style: ViewStyle | None = None,
    ) -> Project:
        """
        Update an existing project.

        Only the fields to be updated need to be provided as keyword arguments.

        :param project_id: The ID of the project to update.
        :param name: The name of the project.
        :param description: Description for the project (up to 1024 characters).
        :param color: The color of the project icon.
        :param is_favorite: Whether the project is a favorite.
        :param view_style: A string value (either 'list' or 'board').
        :return: the updated Project.
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{PROJECTS_PATH}/{project_id}")

        data = kwargs_without_none(
            name=name,
            description=description,
            color=color,
            is_favorite=is_favorite,
            view_style=view_style,
        )

        project_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )
        return Project.from_dict(project_data)

    async def archive_project(self, project_id: str) -> Project:
        """
        Archive a project.

        For personal projects, archives it only for the user.
        For workspace projects, archives it for all members.

        :param project_id: The ID of the project to archive.
        :return: The archived project object.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Project dictionary.
        """
        endpoint = get_api_url(
            f"{PROJECTS_PATH}/{project_id}/{PROJECT_ARCHIVE_PATH_SUFFIX}"
        )
        project_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )
        return Project.from_dict(project_data)

    async def unarchive_project(self, project_id: str) -> Project:
        """
        Unarchive a project.

        Restores a previously archived project.

        :param project_id: The ID of the project to unarchive.
        :return: The unarchived project object.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Project dictionary.
        """
        endpoint = get_api_url(
            f"{PROJECTS_PATH}/{project_id}/{PROJECT_UNARCHIVE_PATH_SUFFIX}"
        )
        project_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )
        return Project.from_dict(project_data)

    async def delete_project(self, project_id: str) -> bool:
        """
        Delete a project.

        All nested sections and tasks will also be deleted.

        :param project_id: The ID of the project to delete.
        :return: True if the project was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{PROJECTS_PATH}/{project_id}")
        return await delete_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )

    async def get_collaborators(
        self,
        project_id: str,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Collaborator]]:
        """
        Get an iterable of lists of collaborators in shared projects.

        The response is an iterable of lists of collaborators in shared projects,
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param project_id: The ID of the project.
        :param limit: Maximum number of collaborators per page.
        :return: An iterable of lists of collaborators.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(f"{PROJECTS_PATH}/{project_id}/{COLLABORATORS_PATH}")
        params = kwargs_without_none(limit=limit)
        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            Collaborator.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def get_section(self, section_id: str) -> Section:
        """
        Get a specific section by its ID.

        :param section_id: The ID of the section to retrieve.
        :return: The requested section.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Section dictionary.
        """
        endpoint = get_api_url(f"{SECTIONS_PATH}/{section_id}")
        section_data: dict[str, Any] = await get_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )
        return Section.from_dict(section_data)

    async def get_sections(
        self,
        project_id: str | None = None,
        *,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Section]]:
        """
        Get an iterable of lists of active sections.

        Supports filtering by `project_id` and pagination arguments.

        The response is an iterable of lists of active sections.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param project_id: Filter sections by project ID.
        :param limit: Maximum number of sections per page.
        :return: An iterable of lists of sections.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(SECTIONS_PATH)

        params = kwargs_without_none(project_id=project_id, limit=limit)

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            Section.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def search_sections(
        self,
        query: Annotated[str, MinLen(1), MaxLen(1024)],
        *,
        project_id: str | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Section]]:
        """
        Search active sections by name.

        The response is an iterable of lists of sections matching the query.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param query: Query string for section names.
        :param project_id: If set, search sections within the given project only.
        :param limit: Maximum number of sections per page.
        :return: An iterable of lists of sections.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(f"{SECTIONS_PATH}/{SECTIONS_SEARCH_PATH_SUFFIX}")

        params = kwargs_without_none(query=query, project_id=project_id, limit=limit)

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            Section.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def add_section(
        self,
        name: Annotated[str, MinLen(1), MaxLen(2048)],
        project_id: str,
        *,
        order: int | None = None,
    ) -> Section:
        """
        Create a new section within a project.

        :param name: The name of the section.
        :param project_id: The ID of the project to add the section to.
        :param order: The order of the section among all sections in the project.
        :return: The newly created section.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Section dictionary.
        """
        endpoint = get_api_url(SECTIONS_PATH)

        data = kwargs_without_none(name=name, project_id=project_id, order=order)

        section_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )
        return Section.from_dict(section_data)

    async def update_section(
        self,
        section_id: str,
        name: Annotated[str, MinLen(1), MaxLen(2048)],
    ) -> Section:
        """
        Update an existing section.

        Currently, only `name` can be updated.

        :param section_id: The ID of the section to update.
        :param name: The new name for the section.
        :return: the updated Section.
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{SECTIONS_PATH}/{section_id}")
        section_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data={"name": name},
        )
        return Section.from_dict(section_data)

    async def delete_section(self, section_id: str) -> bool:
        """
        Delete a section.

        All tasks within the section will also be deleted.

        :param section_id: The ID of the section to delete.
        :return: True if the section was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{SECTIONS_PATH}/{section_id}")
        return await delete_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )

    async def get_comment(self, comment_id: str) -> Comment:
        """
        Get a specific comment by its ID.

        :param comment_id: The ID of the comment to retrieve.
        :return: The requested comment.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Comment dictionary.
        """
        endpoint = get_api_url(f"{COMMENTS_PATH}/{comment_id}")
        comment_data: dict[str, Any] = await get_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )
        return Comment.from_dict(comment_data)

    async def get_comments(
        self,
        *,
        project_id: str | None = None,
        task_id: str | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Comment]]:
        """
        Get an iterable of lists of comments for a task or project.

        Requires either `project_id` or `task_id` to be set.

        The response is an iterable of lists of comments.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param project_id: The ID of the project to retrieve comments for.
        :param task_id: The ID of the task to retrieve comments for.
        :param limit: Maximum number of comments per page.
        :return: An iterable of lists of comments.
        :raises ValueError: If neither `project_id` nor `task_id` is provided.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        if project_id is None and task_id is None:
            raise ValueError("Either `project_id` or `task_id` must be provided.")

        endpoint = get_api_url(COMMENTS_PATH)

        params = kwargs_without_none(
            project_id=project_id,
            task_id=task_id,
            limit=limit,
        )

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            Comment.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def add_comment(
        self,
        content: Annotated[str, MaxLen(15000)],
        *,
        project_id: str | None = None,
        task_id: str | None = None,
        attachment: Attachment | None = None,
        uids_to_notify: list[str] | None = None,
    ) -> Comment:
        """
        Create a new comment on a task or project.

        Requires either `project_id` or `task_id` to be set,
        and can optionally include an `attachment` object.

        :param content: The text content of the comment (supports Markdown).
        :param project_id: The ID of the project to add the comment to.
        :param task_id: The ID of the task to add the comment to.
        :param attachment: The attachment object to include with the comment.
        :param uids_to_notify: A list of user IDs to notify.
        :return: The newly created comment.
        :raises ValueError: If neither `project_id` nor `task_id` is provided.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Comment dictionary.
        """
        if project_id is None and task_id is None:
            raise ValueError("Either `project_id` or `task_id` must be provided.")

        endpoint = get_api_url(COMMENTS_PATH)

        data = kwargs_without_none(
            content=content,
            project_id=project_id,
            task_id=task_id,
            attachment=attachment.to_dict() if attachment is not None else None,
            uids_to_notify=uids_to_notify,
        )

        comment_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )
        return Comment.from_dict(comment_data)

    async def update_comment(
        self, comment_id: str, content: Annotated[str, MaxLen(15000)]
    ) -> Comment:
        """
        Update an existing comment.

        Currently, only `content` can be updated.

        :param comment_id: The ID of the comment to update.
        :param content: The new text content for the comment.
        :return: the updated Comment.
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{COMMENTS_PATH}/{comment_id}")
        comment_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data={"content": content},
        )
        return Comment.from_dict(comment_data)

    async def delete_comment(self, comment_id: str) -> bool:
        """
        Delete a comment.

        :param comment_id: The ID of the comment to delete.
        :return: True if the comment was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{COMMENTS_PATH}/{comment_id}")
        return await delete_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )

    async def get_label(self, label_id: str) -> Label:
        """
        Get a specific personal label by its ID.

        :param label_id: The ID of the label to retrieve.
        :return: The requested label.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Label dictionary.
        """
        endpoint = get_api_url(f"{LABELS_PATH}/{label_id}")
        label_data: dict[str, Any] = await get_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )
        return Label.from_dict(label_data)

    async def get_labels(
        self,
        *,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Label]]:
        """
        Get an iterable of lists of personal labels.

        Supports pagination arguments.

        The response is an iterable of lists of personal labels.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param limit: Maximum number of labels per page.
        :return: An iterable of lists of personal labels.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(LABELS_PATH)

        params = kwargs_without_none(limit=limit)

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            Label.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def search_labels(
        self,
        query: Annotated[str, MinLen(1), MaxLen(1024)],
        *,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[Label]]:
        """
        Search personal labels by name.

        The response is an iterable of lists of labels matching the query.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param query: Query string for label names.
        :param limit: Maximum number of labels per page.
        :return: An iterable of lists of labels.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(f"{LABELS_PATH}/{LABELS_SEARCH_PATH_SUFFIX}")

        params = kwargs_without_none(query=query, limit=limit)

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            Label.from_dict,
            self._token,
            self._request_id_fn,
            params,
        )

    async def add_label(
        self,
        name: Annotated[str, MinLen(1), MaxLen(60)],
        *,
        color: ColorString | None = None,
        item_order: int | None = None,
        is_favorite: bool | None = None,
    ) -> Label:
        """
        Create a new personal label.

        :param name: The name of the label.
        :param color: The color of the label icon.
        :param item_order: Label's order in the label list.
        :param is_favorite: Whether the label is a favorite.
        :return: The newly created label.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response is not a valid Label dictionary.
        """
        endpoint = get_api_url(LABELS_PATH)

        data = kwargs_without_none(
            name=name,
            color=color,
            item_order=item_order,
            is_favorite=is_favorite,
        )

        label_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )
        return Label.from_dict(label_data)

    async def update_label(
        self,
        label_id: str,
        *,
        name: Annotated[str, MinLen(1), MaxLen(60)] | None = None,
        color: ColorString | None = None,
        item_order: int | None = None,
        is_favorite: bool | None = None,
    ) -> Label:
        """
        Update a personal label.

        Only the fields to be updated need to be provided as keyword arguments.

        :param label_id: The ID of the label.
        :param name: The name of the label.
        :param color: The color of the label icon.
        :param item_order: Label's order in the label list.
        :param is_favorite: Whether the label is a favorite.
        :return: the updated Label.
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{LABELS_PATH}/{label_id}")

        data = kwargs_without_none(
            name=name,
            color=color,
            item_order=item_order,
            is_favorite=is_favorite,
        )

        label_data: dict[str, Any] = await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )
        return Label.from_dict(label_data)

    async def delete_label(self, label_id: str) -> bool:
        """
        Delete a personal label.

        Instances of the label will be removed from tasks.

        :param label_id: The ID of the label to delete.
        :return: True if the label was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(f"{LABELS_PATH}/{label_id}")
        return await delete_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
        )

    async def get_shared_labels(
        self,
        *,
        omit_personal: bool = False,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncIterator[list[str]]:
        """
        Get an iterable of lists of shared label names.

        Includes labels from collaborators on shared projects that are not in the
        user's personal labels. Can optionally exclude personal label names using
        `omit_personal=True`. Supports pagination arguments.

        The response is an iterable of lists of shared label names.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param omit_personal: Optional boolean flag to omit personal label names.
        :param limit: Maximum number of labels per page.
        :return: An iterable of lists of shared label names (strings).
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(SHARED_LABELS_PATH)

        params = kwargs_without_none(omit_personal=omit_personal, limit=limit)

        return AsyncResultsPaginator(
            self._client,
            endpoint,
            "results",
            str,
            self._token,
            self._request_id_fn,
            params,
        )

    async def rename_shared_label(
        self,
        name: Annotated[str, MaxLen(60)],
        new_name: Annotated[str, MinLen(1), MaxLen(60)],
    ) -> bool:
        """
        Rename all occurrences of a shared label across all projects.

        :param name: The current name of the shared label to rename.
        :param new_name: The new name for the shared label.
        :return: True if the rename was successful,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(SHARED_LABELS_RENAME_PATH)
        return await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            params={"name": name},
            data={"new_name": new_name},
        )

    async def remove_shared_label(self, name: Annotated[str, MaxLen(60)]) -> bool:
        """
        Remove all occurrences of a shared label across all projects.

        This action removes the label string from all tasks where it appears.

        :param name: The name of the shared label to remove.
        :return: True if the removal was successful,
        :raises httpx.HTTPStatusError: If the API request fails.
        """
        endpoint = get_api_url(SHARED_LABELS_REMOVE_PATH)
        data = {"name": name}
        return await post_async(
            self._client,
            endpoint,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            data=data,
        )


T = TypeVar("T")


class AsyncResultsPaginator(AsyncIterator[list[T]]):
    """
    Iterator for paginated results from the Todoist API.

    It encapsulates the logic for fetching and iterating through paginated results
    from Todoist API endpoints. It handles cursor-based pagination automatically,
    requesting new pages as needed when iterating.
    """

    _client: httpx.AsyncClient
    _url: str
    _results_field: str
    _results_inst: Callable[[Any], T]
    _token: str
    _cursor: str | None

    def __init__(
        self,
        client: httpx.AsyncClient,
        url: str,
        results_field: str,
        results_inst: Callable[[Any], T],
        token: str,
        request_id_fn: Callable[[], str] | None,
        params: dict[str, Any],
    ) -> None:
        """
        Initialize the ResultsPaginator.

        :param client: The httpx client to use for API calls.
        :param url: The API endpoint URL to fetch results from.
        :param results_field: The key in the API response that contains the results.
        :param results_inst: A callable that converts result items to objects of type T.
        :param token: The authentication token for the Todoist API.
        :param params: Query parameters to include in API requests.
        """
        self._client = client
        self._url = url
        self._results_field = results_field
        self._results_inst = results_inst
        self._token = token
        self._request_id_fn = request_id_fn
        self._params = params
        self._cursor = ""  # empty string for first page

    async def __anext__(self) -> list[T]:
        """
        Fetch and return the next page of results from the Todoist API.

        :return: A list of results.
        :raises httpx.HTTPStatusError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        if self._cursor is None:
            raise StopAsyncIteration

        params = self._params.copy()
        if self._cursor != "":
            params["cursor"] = self._cursor

        data: dict[str, Any] = await get_async(
            self._client,
            self._url,
            self._token,
            self._request_id_fn() if self._request_id_fn else None,
            params,
        )
        self._cursor = data.get("next_cursor")

        results: list[Any] = data.get(self._results_field, [])
        return [self._results_inst(result) for result in results]
