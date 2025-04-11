from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Literal, Optional, Union

from dataclass_wizard import JSONPyWizard
from dataclass_wizard.v1 import DatePattern, DateTimePattern, UTCDateTimePattern
from dataclass_wizard.v1.models import Alias

from todoist_api_python._core.endpoints import INBOX_URL, get_project_url, get_task_url

ViewStyle = Literal["list", "board", "calendar"]
DurationUnit = Literal["minute", "day"]
ApiDate = UTCDateTimePattern["%FT%T.%fZ"]  # type: ignore[valid-type]
ApiDue = Union[  # noqa: UP007 # https://github.com/rnag/dataclass-wizard/issues/189
    DatePattern["%F"], DateTimePattern["%FT%T"], UTCDateTimePattern["%FT%TZ"]  # type: ignore[valid-type]  # noqa: F722
]


@dataclass
class Project(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    id: str
    name: str
    description: str
    order: Annotated[int, Alias(load=("child_order", "order"))]
    color: str
    is_collapsed: Annotated[bool, Alias(load=("collapsed", "is_collapsed"))]
    is_shared: Annotated[bool, Alias(load=("shared", "is_shared"))]
    is_favorite: bool
    is_archived: bool
    can_assign_tasks: bool
    view_style: ViewStyle
    created_at: ApiDate
    updated_at: ApiDate

    parent_id: str | None = None
    is_inbox_project: Annotated[
        bool | None, Alias(load=("inbox_project", "is_inbox_project"))
    ] = None

    workspace_id: str | None = None
    folder_id: str | None = None

    @property
    def url(self) -> str:
        if self.is_inbox_project:
            return INBOX_URL
        return get_project_url(self.id, self.name)


@dataclass
class Section(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    id: str
    name: str
    project_id: str
    is_collapsed: Annotated[bool, Alias(load=("collapsed", "is_collapsed"))]
    order: Annotated[int, Alias(load=("section_order", "order"))]


@dataclass
class Due(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    date: ApiDue
    string: str
    lang: str = "en"
    is_recurring: bool = False
    timezone: str | None = None


@dataclass
class Deadline(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    date: ApiDue
    lang: str = "en"


@dataclass
class Meta(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    project: tuple[str, str]
    section: tuple[str, str]
    assignee: tuple[str, str]
    labels: dict[int, str]
    due: Due | None
    deadline: Deadline | None


@dataclass
class Task(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    id: str
    content: str
    description: str
    project_id: str
    section_id: str | None
    parent_id: str | None
    labels: list[str] | None
    priority: int
    due: Due | None
    deadline: Deadline | None
    duration: Duration | None
    is_collapsed: Annotated[bool, Alias(load=("collapsed", "is_collapsed"))]
    order: Annotated[int, Alias(load=("child_order", "order"))]
    assignee_id: Annotated[str | None, Alias(load=("responsible_uid", "assignee_id"))]
    assigner_id: Annotated[str | None, Alias(load=("assigned_by_uid", "assigner_id"))]
    completed_at: Optional[ApiDate]  # noqa: UP007 # https://github.com/rnag/dataclass-wizard/issues/189
    creator_id: Annotated[str, Alias(load=("added_by_uid", "creator_id"))]
    created_at: Annotated[ApiDate, Alias(load=("added_at", "created_at"))]
    updated_at: ApiDate

    meta: Meta | None = None

    @property
    def url(self) -> str:
        return get_task_url(self.id, self.content)

    @property
    def is_completed(self) -> bool:
        return self.completed_at is not None


@dataclass
class Collaborator(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    id: str
    email: str
    name: str


@dataclass
class Attachment(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    resource_type: str | None = None

    file_name: str | None = None
    file_size: int | None = None
    file_type: str | None = None
    file_url: str | None = None
    file_duration: int | None = None
    upload_state: str | None = None

    image: str | None = None
    image_width: int | None = None
    image_height: int | None = None

    url: str | None = None
    title: str | None = None


@dataclass
class Comment(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    id: str
    content: str
    poster_id: Annotated[str, Alias(load=("posted_uid", "poster_id"))]
    posted_at: ApiDate
    task_id: Annotated[str | None, Alias(load=("item_id", "task_id"))] = None
    project_id: str | None = None
    attachment: Annotated[
        Attachment | None, Alias(load=("file_attachment", "attachment"))
    ] = None

    def __post_init__(self) -> None:
        """
        Finish initialization of the Comment object.

        :raises ValueError: If neither `task_id` nor `project_id` is specified.
        """
        if self.task_id is None and self.project_id is None:
            raise ValueError("Must specify `task_id` or `project_id`")


@dataclass
class Label(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    id: str
    name: str
    color: str
    order: int
    is_favorite: bool


@dataclass
class AuthResult(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    access_token: str
    state: str | None


@dataclass
class Duration(JSONPyWizard):
    class _(JSONPyWizard.Meta):  # noqa:N801
        v1 = True

    amount: int
    unit: DurationUnit
