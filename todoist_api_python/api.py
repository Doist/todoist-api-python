from __future__ import annotations

import sys
from collections.abc import Callable, Iterator
from typing import TYPE_CHECKING, Annotated, Any, Literal, TypeVar
from weakref import finalize

import requests
from annotated_types import Ge, Le, MaxLen, MinLen, Predicate

from todoist_api_python._core.endpoints import (
    COLLABORATORS_PATH,
    COMMENTS_PATH,
    LABELS_PATH,
    PROJECT_ARCHIVE_PATH_SUFFIX,
    PROJECT_UNARCHIVE_PATH_SUFFIX,
    PROJECTS_PATH,
    SECTIONS_PATH,
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
from todoist_api_python._core.http_requests import delete, get, post
from todoist_api_python._core.utils import format_date, format_datetime
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

if sys.version_info >= (3, 11):
    from typing import Self
else:
    Self = TypeVar("Self", bound="TodoistAPI")


LanguageCode = Annotated[str, Predicate(lambda x: len(x) == 2)]  # noqa: PLR2004
ColorString = Annotated[
    str,
    Predicate(
        lambda x: x
        in (
            "berry_red",
            "red",
            "orange",
            "yellow",
            "olive_green",
            "lime_green",
            "green",
            "mint_green",
            "teal",
            "sky_blue",
            "light_blue",
            "blue",
            "grape",
            "violet",
            "lavender",
            "magenta",
            "salmon",
            "charcoal",
            "grey",
            "taupe",
        )
    ),
]
ViewStyle = Annotated[str, Predicate(lambda x: x in ("list", "board", "calendar"))]


class TodoistAPI:
    """
    Client for the Todoist API.

    Provides methods for interacting with Todoist resources like tasks, projects,
    labels, comments, etc.

    Manages an HTTP session and handles authentication. Can be used as a context manager
    to ensure the session is closed properly.
    """

    def __init__(self, token: str, session: requests.Session | None = None) -> None:
        """
        Initialize the TodoistAPI client.

        :param token: Authentication token for the Todoist API.
        :param session: An optional pre-configured requests `Session` object.
        """
        self._token: str = token
        self._session = session or requests.Session()
        self._finalizer = finalize(self, self._session.close)

    def __enter__(self) -> Self:
        """
        Enters the runtime context related to this object.

        The with statement will bind this method's return value to the target(s)
        specified in the as clause of the statement, if any.

        :return: This TodoistAPI instance.
        """
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the runtime context and closes the underlying requests session."""
        self._finalizer()

    def get_task(self, task_id: str) -> Task:
        """
        Get a specific task by its ID.

        :param task_id: The ID of the task to retrieve.
        :return: The requested task.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Task dictionary.
        """
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}")
        task_data: dict[str, Any] = get(self._session, endpoint, self._token)
        return Task.from_dict(task_data)

    def get_tasks(
        self,
        *,
        project_id: str | None = None,
        section_id: str | None = None,
        parent_id: str | None = None,
        label: str | None = None,
        ids: list[str] | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> Iterator[list[Task]]:
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(TASKS_PATH)

        params: dict[str, Any] = {}
        if project_id is not None:
            params["project_id"] = project_id
        if section_id is not None:
            params["section_id"] = section_id
        if parent_id is not None:
            params["parent_id"] = parent_id
        if label is not None:
            params["label"] = label
        if ids is not None:
            params["ids"] = ",".join(str(i) for i in ids)
        if limit is not None:
            params["limit"] = limit

        return ResultsPaginator(
            self._session,
            endpoint,
            "results",
            Task.from_dict,
            self._token,
            params,
        )

    def filter_tasks(
        self,
        *,
        query: Annotated[str, MaxLen(1024)] | None = None,
        lang: str | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> Iterator[list[Task]]:
        """
        Get an iterable of lists of active tasks matching the filter.

        The response is an iterable of lists of active tasks matching the criteria.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param query: Query tasks using Todoist's filter language.
        :param lang: Language for task content (e.g., 'en').
        :param limit: Maximum number of tasks per page.
        :return: An iterable of lists of tasks.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(TASKS_FILTER_PATH)

        params: dict[str, Any] = {}
        if query is not None:
            params["query"] = query
        if lang is not None:
            params["lang"] = lang
        if limit is not None:
            params["limit"] = limit

        return ResultsPaginator(
            self._session,
            endpoint,
            "results",
            Task.from_dict,
            self._token,
            params,
        )

    def add_task(  # noqa: PLR0912
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Task dictionary.
        """
        endpoint = get_api_url(TASKS_PATH)

        data: dict[str, Any] = {"content": content}
        if description is not None:
            data["description"] = description
        if project_id is not None:
            data["project_id"] = project_id
        if section_id is not None:
            data["section_id"] = section_id
        if parent_id is not None:
            data["parent_id"] = parent_id
        if labels is not None:
            data["labels"] = labels
        if priority is not None:
            data["priority"] = priority
        if due_string is not None:
            data["due_string"] = due_string
        if due_lang is not None:
            data["due_lang"] = due_lang
        if due_date is not None:
            data["due_date"] = format_date(due_date)
        if due_datetime is not None:
            data["due_datetime"] = format_datetime(due_datetime)
        if assignee_id is not None:
            data["assignee_id"] = assignee_id
        if order is not None:
            data["order"] = order
        if auto_reminder is not None:
            data["auto_reminder"] = auto_reminder
        if auto_parse_labels is not None:
            data["auto_parse_labels"] = auto_parse_labels
        if duration is not None:
            data["duration"] = duration
        if duration_unit is not None:
            data["duration_unit"] = duration_unit
        if deadline_date is not None:
            data["deadline_date"] = format_date(deadline_date)
        if deadline_lang is not None:
            data["deadline_lang"] = deadline_lang

        task_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data=data
        )
        return Task.from_dict(task_data)

    def add_task_quick(
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response cannot be parsed into a QuickAddResult.
        """
        endpoint = get_api_url(TASKS_QUICK_ADD_PATH)

        data = {
            "meta": True,
            "text": text,
            "auto_reminder": auto_reminder,
        }

        if note is not None:
            data["note"] = note
        if reminder is not None:
            data["reminder"] = reminder

        task_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data=data
        )
        return Task.from_dict(task_data)

    def update_task(  # noqa: PLR0912
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}")

        data: dict[str, Any] = {}
        if content is not None:
            data["content"] = content
        if description is not None:
            data["description"] = description
        if labels is not None:
            data["labels"] = labels
        if priority is not None:
            data["priority"] = priority
        if due_string is not None:
            data["due_string"] = due_string
        if due_lang is not None:
            data["due_lang"] = due_lang
        if due_date is not None:
            data["due_date"] = format_date(due_date)
        if due_datetime is not None:
            data["due_datetime"] = format_datetime(due_datetime)
        if assignee_id is not None:
            data["assignee_id"] = assignee_id
        if day_order is not None:
            data["day_order"] = day_order
        if collapsed is not None:
            data["collapsed"] = collapsed
        if duration is not None:
            data["duration"] = duration
        if duration_unit is not None:
            data["duration_unit"] = duration_unit
        if deadline_date is not None:
            data["deadline_date"] = format_date(deadline_date)
        if deadline_lang is not None:
            data["deadline_lang"] = deadline_lang

        task_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data=data
        )
        return Task.from_dict(task_data)

    def complete_task(self, task_id: str) -> bool:
        """
        Complete a task.

        For recurring tasks, this schedules the next occurrence.
        For non-recurring tasks, it marks them as completed.

        :param task_id: The ID of the task to close.
        :return: True if the task was closed successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}/close")
        return post(self._session, endpoint, self._token)

    def uncomplete_task(self, task_id: str) -> bool:
        """
        Uncomplete a (completed) task.

        Any parent tasks or sections will also be uncompleted.

        :param task_id: The ID of the task to reopen.
        :return: True if the task was uncompleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}/reopen")
        return post(self._session, endpoint, self._token)

    def move_task(
        self,
        task_id: str,
        project_id: str | None = None,
        section_id: str | None = None,
        parent_id: str | None = None,
    ) -> bool:
        """
        Move a task.

        Move a task to a different project, section, or parent task.
        Project_id takes precedence.
        Moving a task to a section or parent will update its project to match
        the project of the section or parent task.

        :param task_id: The ID of the task to reopen.
        :param project_id: The ID of the project to add the task to.
        :param section_id: The ID of the section to add the task to.
        :param parent_id: The ID of the parent task.
        :return: True if the task was moved successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        data: dict[str, Any] = {}
        if project_id is not None:
            data["project_id"] = project_id
        if section_id is not None:
            data["section_id"] = section_id
        if parent_id is not None:
            data["parent_id"] = parent_id
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}/move")
        return post(self._session, endpoint, self._token, data=data)

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        :param task_id: The ID of the task to delete.
        :return: True if the task was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{TASKS_PATH}/{task_id}")
        return delete(self._session, endpoint, self._token)

    def get_completed_tasks_by_due_date(
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
    ) -> Iterator[list[Task]]:
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(TASKS_COMPLETED_BY_DUE_DATE_PATH)

        params: dict[str, Any] = {
            "since": format_datetime(since),
            "until": format_datetime(until),
        }
        if workspace_id is not None:
            params["workspace_id"] = workspace_id
        if project_id is not None:
            params["project_id"] = project_id
        if section_id is not None:
            params["section_id"] = section_id
        if parent_id is not None:
            params["parent_id"] = parent_id
        if filter_query is not None:
            params["filter_query"] = filter_query
        if filter_lang is not None:
            params["filter_lang"] = filter_lang
        if limit is not None:
            params["limit"] = limit

        return ResultsPaginator(
            self._session, endpoint, "items", Task.from_dict, self._token, params
        )

    def get_completed_tasks_by_completion_date(
        self,
        *,
        since: datetime,
        until: datetime,
        workspace_id: str | None = None,
        filter_query: str | None = None,
        filter_lang: str | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> Iterator[list[Task]]:
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(TASKS_COMPLETED_BY_COMPLETION_DATE_PATH)

        params: dict[str, Any] = {
            "since": format_datetime(since),
            "until": format_datetime(until),
        }
        if workspace_id is not None:
            params["workspace_id"] = workspace_id
        if filter_query is not None:
            params["filter_query"] = filter_query
        if filter_lang is not None:
            params["filter_lang"] = filter_lang
        if limit is not None:
            params["limit"] = limit

        return ResultsPaginator(
            self._session, endpoint, "items", Task.from_dict, self._token, params
        )

    def get_project(self, project_id: str) -> Project:
        """
        Get a project by its ID.

        :param project_id: The ID of the project to retrieve.
        :return: The requested project.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Project dictionary.
        """
        endpoint = get_api_url(f"{PROJECTS_PATH}/{project_id}")
        project_data: dict[str, Any] = get(self._session, endpoint, self._token)
        return Project.from_dict(project_data)

    def get_projects(
        self,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> Iterator[list[Project]]:
        """
        Get an iterable of lists of active projects.

        The response is an iterable of lists of active projects.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param limit: Maximum number of projects per page.
        :return: An iterable of lists of projects.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(PROJECTS_PATH)
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        return ResultsPaginator(
            self._session, endpoint, "results", Project.from_dict, self._token, params
        )

    def add_project(
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Project dictionary.
        """
        endpoint = get_api_url(PROJECTS_PATH)

        data: dict[str, Any] = {"name": name}
        if parent_id is not None:
            data["parent_id"] = parent_id
        if description is not None:
            data["description"] = description
        if color is not None:
            data["color"] = color
        if is_favorite is not None:
            data["is_favorite"] = is_favorite
        if view_style is not None:
            data["view_style"] = view_style

        project_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data=data
        )
        return Project.from_dict(project_data)

    def update_project(
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{PROJECTS_PATH}/{project_id}")

        data: dict[str, Any] = {}

        if name is not None:
            data["name"] = name
        if description is not None:
            data["description"] = description
        if color is not None:
            data["color"] = color
        if is_favorite is not None:
            data["is_favorite"] = is_favorite
        if view_style is not None:
            data["view_style"] = view_style

        project_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data=data
        )
        return Project.from_dict(project_data)

    def archive_project(self, project_id: str) -> Project:
        """
        Archive a project.

        For personal projects, archives it only for the user.
        For workspace projects, archives it for all members.

        :param project_id: The ID of the project to archive.
        :return: The archived project object.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Project dictionary.
        """
        endpoint = get_api_url(
            f"{PROJECTS_PATH}/{project_id}/{PROJECT_ARCHIVE_PATH_SUFFIX}"
        )
        project_data: dict[str, Any] = post(self._session, endpoint, self._token)
        return Project.from_dict(project_data)

    def unarchive_project(self, project_id: str) -> Project:
        """
        Unarchive a project.

        Restores a previously archived project.

        :param project_id: The ID of the project to unarchive.
        :return: The unarchived project object.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Project dictionary.
        """
        endpoint = get_api_url(
            f"{PROJECTS_PATH}/{project_id}/{PROJECT_UNARCHIVE_PATH_SUFFIX}"
        )
        project_data: dict[str, Any] = post(self._session, endpoint, self._token)
        return Project.from_dict(project_data)

    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project.

        All nested sections and tasks will also be deleted.

        :param project_id: The ID of the project to delete.
        :return: True if the project was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{PROJECTS_PATH}/{project_id}")
        return delete(self._session, endpoint, self._token)

    def get_collaborators(
        self,
        project_id: str,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> Iterator[list[Collaborator]]:
        """
        Get an iterable of lists of collaborators in shared projects.

        The response is an iterable of lists of collaborators in shared projects,
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param project_id: The ID of the project.
        :param limit: Maximum number of collaborators per page.
        :return: An iterable of lists of collaborators.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(f"{PROJECTS_PATH}/{project_id}/{COLLABORATORS_PATH}")
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        return ResultsPaginator(
            self._session,
            endpoint,
            "results",
            Collaborator.from_dict,
            self._token,
            params,
        )

    def get_section(self, section_id: str) -> Section:
        """
        Get a specific section by its ID.

        :param section_id: The ID of the section to retrieve.
        :return: The requested section.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Section dictionary.
        """
        endpoint = get_api_url(f"{SECTIONS_PATH}/{section_id}")
        section_data: dict[str, Any] = get(self._session, endpoint, self._token)
        return Section.from_dict(section_data)

    def get_sections(
        self,
        project_id: str | None = None,
        *,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> Iterator[list[Section]]:
        """
        Get an iterable of lists of active sections.

        Supports filtering by `project_id` and pagination arguments.

        The response is an iterable of lists of active sections.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param project_id: Filter sections by project ID.
        :param limit: Maximum number of sections per page.
        :return: An iterable of lists of sections.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(SECTIONS_PATH)

        params: dict[str, Any] = {}
        if project_id is not None:
            params["project_id"] = project_id
        if limit is not None:
            params["limit"] = limit

        return ResultsPaginator(
            self._session, endpoint, "results", Section.from_dict, self._token, params
        )

    def add_section(
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Section dictionary.
        """
        endpoint = get_api_url(SECTIONS_PATH)

        data: dict[str, Any] = {"name": name, "project_id": project_id}
        if order is not None:
            data["order"] = order

        section_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data=data
        )
        return Section.from_dict(section_data)

    def update_section(
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{SECTIONS_PATH}/{section_id}")
        section_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data={"name": name}
        )
        return Section.from_dict(section_data)

    def delete_section(self, section_id: str) -> bool:
        """
        Delete a section.

        All tasks within the section will also be deleted.

        :param section_id: The ID of the section to delete.
        :return: True if the section was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{SECTIONS_PATH}/{section_id}")
        return delete(self._session, endpoint, self._token)

    def get_comment(self, comment_id: str) -> Comment:
        """
        Get a specific comment by its ID.

        :param comment_id: The ID of the comment to retrieve.
        :return: The requested comment.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Comment dictionary.
        """
        endpoint = get_api_url(f"{COMMENTS_PATH}/{comment_id}")
        comment_data: dict[str, Any] = get(self._session, endpoint, self._token)
        return Comment.from_dict(comment_data)

    def get_comments(
        self,
        *,
        project_id: str | None = None,
        task_id: str | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> Iterator[list[Comment]]:
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        if project_id is None and task_id is None:
            raise ValueError("Either `project_id` or `task_id` must be provided.")

        endpoint = get_api_url(COMMENTS_PATH)

        params: dict[str, Any] = {}
        if project_id is not None:
            params["project_id"] = project_id
        if task_id is not None:
            params["task_id"] = task_id
        if limit is not None:
            params["limit"] = limit

        return ResultsPaginator(
            self._session, endpoint, "results", Comment.from_dict, self._token, params
        )

    def add_comment(
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Comment dictionary.
        """
        if project_id is None and task_id is None:
            raise ValueError("Either `project_id` or `task_id` must be provided.")

        endpoint = get_api_url(COMMENTS_PATH)

        data: dict[str, Any] = {"content": content}
        if project_id is not None:
            data["project_id"] = project_id
        if task_id is not None:
            data["task_id"] = task_id
        if attachment is not None:
            data["attachment"] = attachment.to_dict()
        if uids_to_notify is not None:
            data["uids_to_notify"] = uids_to_notify

        comment_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data=data
        )
        return Comment.from_dict(comment_data)

    def update_comment(
        self, comment_id: str, content: Annotated[str, MaxLen(15000)]
    ) -> Comment:
        """
        Update an existing comment.

        Currently, only `content` can be updated.

        :param comment_id: The ID of the comment to update.
        :param content: The new text content for the comment.
        :return: the updated Comment.
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{COMMENTS_PATH}/{comment_id}")
        comment_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data={"content": content}
        )
        return Comment.from_dict(comment_data)

    def delete_comment(self, comment_id: str) -> bool:
        """
        Delete a comment.

        :param comment_id: The ID of the comment to delete.
        :return: True if the comment was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{COMMENTS_PATH}/{comment_id}")
        return delete(self._session, endpoint, self._token)

    def get_label(self, label_id: str) -> Label:
        """
        Get a specific personal label by its ID.

        :param label_id: The ID of the label to retrieve.
        :return: The requested label.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Label dictionary.
        """
        endpoint = get_api_url(f"{LABELS_PATH}/{label_id}")
        label_data: dict[str, Any] = get(self._session, endpoint, self._token)
        return Label.from_dict(label_data)

    def get_labels(
        self,
        *,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> Iterator[list[Label]]:
        """
        Get an iterable of lists of personal labels.

        Supports pagination arguments.

        The response is an iterable of lists of personal labels.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param limit: ` number of labels per page.
        :return: An iterable of lists of personal labels.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(LABELS_PATH)

        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit

        return ResultsPaginator(
            self._session, endpoint, "results", Label.from_dict, self._token, params
        )

    def add_label(
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Label dictionary.
        """
        endpoint = get_api_url(LABELS_PATH)

        data: dict[str, Any] = {"name": name}

        if color is not None:
            data["color"] = color
        if item_order is not None:
            data["item_order"] = item_order
        if is_favorite is not None:
            data["is_favorite"] = is_favorite

        label_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data=data
        )
        return Label.from_dict(label_data)

    def update_label(
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{LABELS_PATH}/{label_id}")

        data: dict[str, Any] = {}
        if name is not None:
            data["name"] = name
        if color is not None:
            data["color"] = color
        if item_order is not None:
            data["item_order"] = item_order
        if is_favorite is not None:
            data["is_favorite"] = is_favorite

        label_data: dict[str, Any] = post(
            self._session, endpoint, self._token, data=data
        )
        return Label.from_dict(label_data)

    def delete_label(self, label_id: str) -> bool:
        """
        Delete a personal label.

        Instances of the label will be removed from tasks.

        :param label_id: The ID of the label to delete.
        :return: True if the label was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(f"{LABELS_PATH}/{label_id}")
        return delete(self._session, endpoint, self._token)

    def get_shared_labels(
        self,
        *,
        omit_personal: bool = False,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> Iterator[list[str]]:
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        endpoint = get_api_url(SHARED_LABELS_PATH)

        params: dict[str, Any] = {"omit_personal": omit_personal}
        if limit is not None:
            params["limit"] = limit

        return ResultsPaginator(
            self._session, endpoint, "results", str, self._token, params
        )

    def rename_shared_label(
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
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(SHARED_LABELS_RENAME_PATH)
        return post(
            self._session,
            endpoint,
            self._token,
            params={"name": name},
            data={"new_name": new_name},
        )

    def remove_shared_label(self, name: Annotated[str, MaxLen(60)]) -> bool:
        """
        Remove all occurrences of a shared label across all projects.

        This action removes the label string from all tasks where it appears.

        :param name: The name of the shared label to remove.
        :return: True if the removal was successful,
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        endpoint = get_api_url(SHARED_LABELS_REMOVE_PATH)
        data = {"name": name}
        return post(self._session, endpoint, self._token, data=data)


T = TypeVar("T")


class ResultsPaginator(Iterator[list[T]]):
    """
    Iterator for paginated results from the Todoist API.

    It encapsulates the logic for fetching and iterating through paginated results
    from Todoist API endpoints. It handles cursor-based pagination automatically,
    requesting new pages as needed when iterating.
    """

    _session: requests.Session
    _url: str
    _results_field: str
    _results_inst: Callable[[Any], T]
    _token: str
    _cursor: str | None

    def __init__(
        self,
        session: requests.Session,
        url: str,
        results_field: str,
        results_inst: Callable[[Any], T],
        token: str,
        params: dict[str, Any],
    ) -> None:
        """
        Initialize the ResultsPaginator.

        :param session: The requests Session to use for API calls.
        :param url: The API endpoint URL to fetch results from.
        :param results_field: The key in the API response that contains the results.
        :param results_inst: A callable that converts result items to objects of type T.
        :param token: The authentication token for the Todoist API.
        :param params: Query parameters to include in API requests.
        """
        self._session = session
        self._url = url
        self._results_field = results_field
        self._results_inst = results_inst
        self._token = token
        self._params = params
        self._cursor = ""  # empty string for first page

    def __next__(self) -> list[T]:
        """
        Fetch and return the next page of results from the Todoist API.

        :return: A list of results.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        if self._cursor is None:
            raise StopIteration

        params = self._params.copy()
        if self._cursor != "":
            params["cursor"] = self._cursor

        data: dict[str, Any] = get(self._session, self._url, self._token, params)
        self._cursor = data.get("next_cursor")

        results: list[Any] = data.get(self._results_field, [])
        return [self._results_inst(result) for result in results]
