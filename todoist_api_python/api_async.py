from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Literal, Self

from annotated_types import Ge, Le, MaxLen, MinLen

from todoist_api_python._core.utils import generate_async, run_async
from todoist_api_python.api import TodoistAPI

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator
    from datetime import date, datetime
    from types import TracebackType

    import requests

    from todoist_api_python.models import (
        Attachment,
        Collaborator,
        Comment,
        Label,
        Project,
        Section,
        Task,
    )

from todoist_api_python.api import (
    ColorString,
    LanguageCode,
    ViewStyle,
)


class TodoistAPIAsync:
    """
    Async client for the Todoist API.

    Provides asynchronous methods for interacting with Todoist resources like tasks,
    projects,labels, comments, etc.

    Manages an HTTP session and handles authentication. Can be used as an async context
    manager to ensure the session is closed properly.
    """

    def __init__(self, token: str, session: requests.Session | None = None) -> None:
        """
        Initialize the TodoistAPIAsync client.

        :param token: Authentication token for the Todoist API.
        :param session: An optional pre-configured requests `Session` object.
        """
        self._api = TodoistAPI(token, session)

    async def __aenter__(self) -> Self:
        """
        Enters the async runtime context related to this object.

        The with statement will bind this method's return value to the target(s)
        specified in the as clause of the statement, if any.

        :return: The TodoistAPIAsync instance.
        """
        return self

    def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        traceback: TracebackType | None,
    ) -> None:
        """Exit the async runtime context and closes the underlying requests session."""

    async def get_task(self, task_id: str) -> Task:
        """
        Get a specific task by its ID.

        :param task_id: The ID of the task to retrieve.
        :return: The requested task.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Task dictionary.
        """
        return await run_async(lambda: self._api.get_task(task_id))

    async def get_tasks(
        self,
        *,
        project_id: str | None = None,
        section_id: str | None = None,
        parent_id: str | None = None,
        label: str | None = None,
        ids: list[str] | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncGenerator[list[Task]]:
        """
        Get a list of active tasks.

        :param project_id: Filter tasks by project ID.
        :param section_id: Filter tasks by section ID.
        :param parent_id: Filter tasks by parent task ID.
        :param label: Filter tasks by label name.
        :param ids: A list of the IDs of the tasks to retrieve.
        :param limit: Maximum number of tasks per page (between 1 and 200).
        :return: A list of tasks.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        paginator = self._api.get_tasks(
            project_id=project_id,
            section_id=section_id,
            parent_id=parent_id,
            label=label,
            ids=ids,
            limit=limit,
        )
        return generate_async(paginator)

    async def filter_tasks(
        self,
        *,
        query: Annotated[str, MaxLen(1024)] | None = None,
        lang: str | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncGenerator[list[Task]]:
        """
        Get a lists of active tasks matching the filter.

        The response is an iterable of lists of active tasks matching the criteria.
        Be aware that each iteration fires off a network request to the Todoist API,
        and may result in rate limiting or other API restrictions.

        :param query: Query tasks using Todoist's filter language.
        :param lang: Language for task content (e.g., 'en').
        :param limit: Maximum number of tasks per page (between 1 and 200).
        :return: An iterable of lists of tasks.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        paginator = self._api.filter_tasks(
            query=query,
            lang=lang,
            limit=limit,
        )
        return generate_async(paginator)

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
        due_date: date | None = None,
        due_datetime: datetime | None = None,
        due_lang: LanguageCode | None = None,
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
        return await run_async(
            lambda: self._api.add_task(
                content,
                description=description,
                project_id=project_id,
                section_id=section_id,
                parent_id=parent_id,
                labels=labels,
                priority=priority,
                due_string=due_string,
                due_lang=due_lang,
                due_date=due_date,
                due_datetime=due_datetime,
                assignee_id=assignee_id,
                order=order,
                auto_reminder=auto_reminder,
                auto_parse_labels=auto_parse_labels,
                duration=duration,
                duration_unit=duration_unit,
                deadline_date=deadline_date,
                deadline_lang=deadline_lang,
            )
        )

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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response cannot be parsed into a QuickAddResult.
        """
        return await run_async(
            lambda: self._api.add_task_quick(
                text, note=note, reminder=reminder, auto_reminder=auto_reminder
            )
        )

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
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(
            lambda: self._api.update_task(
                task_id,
                content=content,
                description=description,
                labels=labels,
                priority=priority,
                due_string=due_string,
                due_date=due_date,
                due_datetime=due_datetime,
                due_lang=due_lang,
                assignee_id=assignee_id,
                day_order=day_order,
                collapsed=collapsed,
                duration=duration,
                duration_unit=duration_unit,
                deadline_date=deadline_date,
                deadline_lang=deadline_lang,
            )
        )

    async def complete_task(self, task_id: str) -> bool:
        """
        Complete a task.

        For recurring tasks, this schedules the next occurrence.
        For non-recurring tasks, it marks them as completed.

        :param task_id: The ID of the task to close.
        :return: True if the task was closed successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(lambda: self._api.complete_task(task_id))

    async def uncomplete_task(self, task_id: str) -> bool:
        """
        Uncomplete a (completed) task.

        Any parent tasks or sections will also be uncompleted.

        :param task_id: The ID of the task to reopen.
        :return: True if the task was uncompleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :rtype: bool
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(lambda: self._api.uncomplete_task(task_id))

    async def delete_task(self, task_id: str) -> bool:
        """
        Delete a task.

        :param task_id: The ID of the task to delete.
        :return: True if the task was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(lambda: self._api.delete_task(task_id))

    async def get_project(self, project_id: str) -> Project:
        """
        Get a project by its ID.

        :param project_id: The ID of the project to retrieve.
        :return: The requested project.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Project dictionary.
        """
        return await run_async(lambda: self._api.get_project(project_id))

    async def get_projects(
        self,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncGenerator[list[Project]]:
        """
        Get a list of active projects.

        :param limit: Maximum number of projects per page.
        :return: A list of projects.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        paginator = self._api.get_projects(limit=limit)
        return generate_async(paginator)

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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Project dictionary.
        """
        return await run_async(
            lambda: self._api.add_project(
                name,
                description=description,
                parent_id=parent_id,
                color=color,
                is_favorite=is_favorite,
                view_style=view_style,
            )
        )

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
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(
            lambda: self._api.update_project(
                project_id,
                name=name,
                description=description,
                color=color,
                is_favorite=is_favorite,
                view_style=view_style,
            )
        )

    async def delete_project(self, project_id: str) -> bool:
        """
        Delete a project.

        All nested sections and tasks will also be deleted.

        :param project_id: The ID of the project to delete.
        :return: True if the project was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(lambda: self._api.delete_project(project_id))

    async def get_collaborators(
        self,
        project_id: str,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncGenerator[list[Collaborator]]:
        """
        Get a list of collaborators in shared projects.

        :param project_id: The ID of the project.
        :param limit: Maximum number of collaborators per page.
        :return: A list of collaborators.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        paginator = self._api.get_collaborators(project_id, limit=limit)
        return generate_async(paginator)

    async def get_section(self, section_id: str) -> Section:
        """
        Get a specific section by its ID.

        :param section_id: The ID of the section to retrieve.
        :return: The requested section.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Section dictionary.
        """
        return await run_async(lambda: self._api.get_section(section_id))

    async def get_sections(
        self,
        project_id: str | None = None,
        *,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncGenerator[list[Section]]:
        """
        Get a list of active sections.

        Supports filtering by `project_id` and pagination arguments.

        :param project_id: Filter sections by project ID.
        :param limit: Maximum number of sections per page (between 1 and 200).
        :return: A list of sections.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        paginator = self._api.get_sections(project_id=project_id, limit=limit)
        return generate_async(paginator)

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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Section dictionary.
        """
        return await run_async(
            lambda: self._api.add_section(name, project_id, order=order)
        )

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
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(lambda: self._api.update_section(section_id, name))

    async def delete_section(self, section_id: str) -> bool:
        """
        Delete a section.

        All tasks within the section will also be deleted.

        :param section_id: The ID of the section to delete.
        :return: True if the section was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(lambda: self._api.delete_section(section_id))

    async def get_comment(self, comment_id: str) -> Comment:
        """
        Get a specific comment by its ID.

        :param comment_id: The ID of the comment to retrieve.
        :return: The requested comment.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Comment dictionary.
        """
        return await run_async(lambda: self._api.get_comment(comment_id))

    async def get_comments(
        self,
        *,
        project_id: str | None = None,
        task_id: str | None = None,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncGenerator[list[Comment]]:
        """
        Get a list of comments for a task or project.

        Requires either `project_id` or `task_id` to be set.

        :param project_id: The ID of the project to retrieve comments for.
        :param task_id: The ID of the task to retrieve comments for.
        :param limit: Maximum number of comments per page (between 1 and 200).
        :return: A list of comments.
        :raises ValueError: If neither `project_id` nor `task_id` is provided.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        paginator = self._api.get_comments(
            project_id=project_id, task_id=task_id, limit=limit
        )
        return generate_async(paginator)

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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Comment dictionary.
        """
        return await run_async(
            lambda: self._api.add_comment(
                content,
                project_id=project_id,
                task_id=task_id,
                attachment=attachment,
                uids_to_notify=uids_to_notify,
            )
        )

    async def update_comment(
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
        return await run_async(lambda: self._api.update_comment(comment_id, content))

    async def delete_comment(self, comment_id: str) -> bool:
        """
        Delete a comment.

        :param comment_id: The ID of the comment to delete.
        :return: True if the comment was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(lambda: self._api.delete_comment(comment_id))

    async def get_label(self, label_id: str) -> Label:
        """
        Get a specific personal label by its ID.

        :param label_id: The ID of the label to retrieve.
        :return: The requested label.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Label dictionary.
        """
        return await run_async(lambda: self._api.get_label(label_id))

    async def get_labels(
        self,
        *,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncGenerator[list[Label]]:
        """
        Get a list of personal labels.

        Supports pagination arguments.

        :param limit: Maximum number of labels per page (between 1 and 200).
        :return: A list of personal labels.
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        paginator = self._api.get_labels(limit=limit)
        return generate_async(paginator)

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
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response is not a valid Label dictionary.
        """
        return await run_async(
            lambda: self._api.add_label(
                name, color=color, item_order=item_order, is_favorite=is_favorite
            )
        )

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
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(
            lambda: self._api.update_label(
                label_id,
                name=name,
                color=color,
                item_order=item_order,
                is_favorite=is_favorite,
            )
        )

    async def delete_label(self, label_id: str) -> bool:
        """
        Delete a personal label.

        Instances of the label will be removed from tasks.

        :param label_id: The ID of the label to delete.
        :return: True if the label was deleted successfully,
                 False otherwise (possibly raise `HTTPError` instead).
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(lambda: self._api.delete_label(label_id))

    async def get_shared_labels(
        self,
        *,
        omit_personal: bool = False,
        limit: Annotated[int, Ge(1), Le(200)] | None = None,
    ) -> AsyncGenerator[list[str]]:
        """
        Get a list of shared label names.

        Includes labels from collaborators on shared projects that are not in the
        user's personal labels. Can optionally exclude personal label names using
        `omit_personal=True`. Supports pagination arguments.

        :param omit_personal: Optional boolean flag to omit personal label names.
        :param limit: Maximum number of labels per page (between 1 and 200).
        :return: A list of shared label names (strings).
        :raises requests.exceptions.HTTPError: If the API request fails.
        :raises TypeError: If the API response structure is unexpected.
        """
        paginator = self._api.get_shared_labels(
            omit_personal=omit_personal, limit=limit
        )
        return generate_async(paginator)

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
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(lambda: self._api.rename_shared_label(name, new_name))

    async def remove_shared_label(self, name: Annotated[str, MaxLen(60)]) -> bool:
        """
        Remove all occurrences of a shared label across all projects.

        This action removes the label string from all tasks where it appears.

        :param name: The name of the shared label to remove.
        :return: True if the removal was successful,
        :raises requests.exceptions.HTTPError: If the API request fails.
        """
        return await run_async(lambda: self._api.remove_shared_label(name))
