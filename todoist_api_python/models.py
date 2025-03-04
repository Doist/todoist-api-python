from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

from dataclasses_json import DataClassJsonMixin

from todoist_api_python.utils import get_url_for_task

VIEW_STYLE = Literal["list", "board"]


@dataclass
class Project(DataClassJsonMixin):
    color: str
    comment_count: int
    id: str
    is_favorite: bool
    is_inbox_project: bool | None
    is_shared: bool
    is_team_inbox: bool | None
    can_assign_tasks: bool | None
    name: str
    order: int
    parent_id: str | None
    url: str
    view_style: VIEW_STYLE


@dataclass
class Section(DataClassJsonMixin):
    id: str
    name: str
    order: int
    project_id: str


@dataclass
class Due(DataClassJsonMixin):
    date: str
    is_recurring: bool
    string: str

    datetime: str | None = None
    timezone: str | None = None

    @classmethod
    def from_quick_add_response(cls, obj: dict[str, Any]) -> Due | None:
        due = obj.get("due")

        if not due:
            return None

        timezone = due.get("timezone")
        datetime: str | None = due["date"] if timezone is not None else None

        due["datetime"] = datetime
        due["timezone"] = timezone

        return cls.from_dict(due)


@dataclass
class Task(DataClassJsonMixin):
    assignee_id: str | None
    assigner_id: str | None
    comment_count: int
    is_completed: bool
    content: str
    created_at: str
    creator_id: str
    description: str
    due: Due | None
    id: str
    labels: list[str] | None
    order: int
    parent_id: str | None
    priority: int
    project_id: str
    section_id: str | None
    url: str = field(init=False)
    duration: Duration | None = None

    sync_id: str | None = None

    def __post_init__(self) -> None:
        self.url = get_url_for_task(
            int(self.id), int(self.sync_id) if self.sync_id else None
        )

    @classmethod
    def from_quick_add_response(cls, obj: dict[str, Any]) -> Task:
        obj_copy = obj.copy()
        obj_copy["due"] = (
            Due.from_quick_add_response(obj) if obj.get("due") is not None else None
        )
        obj_copy["comment_count"] = 0
        obj_copy["is_completed"] = False
        obj_copy["created_at"] = obj_copy.pop("added_at", None)
        obj_copy["creator_id"] = obj_copy.pop("added_by_uid", None)
        obj_copy["assignee_id"] = obj_copy.pop("responsible_uid", None)
        obj_copy["assigner_id"] = obj_copy.pop("assigned_by_uid", None)
        obj_copy["order"] = obj_copy.pop("child_order", None)

        return cls.from_dict(obj_copy)


@dataclass
class QuickAddResult(DataClassJsonMixin):
    task: Task

    resolved_project_name: str | None = None
    resolved_assignee_name: str | None = None
    resolved_label_names: list[str] | None = None
    resolved_section_name: str | None = None

    @classmethod
    def from_quick_add_response(cls, obj: dict[str, Any]) -> QuickAddResult:
        project_data = obj["meta"].get("project", {})
        assignee_data = obj["meta"].get("assignee", {})
        section_data = obj["meta"].get("section", {})

        resolved_project_name = None
        resolved_assignee_name = None
        resolved_section_name = None

        if project_data and len(project_data) == 2:
            resolved_project_name = obj["meta"]["project"][1]

        if assignee_data and len(assignee_data) == 2:
            resolved_assignee_name = obj["meta"]["assignee"][1]

        if section_data and len(section_data) == 2:
            resolved_section_name = obj["meta"]["section"][1]

        resolved_label_names = list(obj["meta"]["labels"].values())

        return cls(
            task=Task.from_quick_add_response(obj),
            resolved_project_name=resolved_project_name,
            resolved_assignee_name=resolved_assignee_name,
            resolved_label_names=resolved_label_names,
            resolved_section_name=resolved_section_name,
        )


@dataclass
class Collaborator(DataClassJsonMixin):
    id: str
    email: str
    name: str


@dataclass
class Attachment(DataClassJsonMixin):
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
class Comment(DataClassJsonMixin):
    content: str
    id: str
    posted_at: str
    project_id: str | None
    task_id: str | None
    attachment: Attachment | None = None


@dataclass
class Label(DataClassJsonMixin):
    id: str
    name: str
    color: str
    order: int
    is_favorite: bool


@dataclass
class AuthResult(DataClassJsonMixin):
    access_token: str
    state: str | None


@dataclass
class Item(DataClassJsonMixin):
    id: str
    user_id: str
    project_id: str
    content: str
    description: str
    priority: int
    child_order: int
    collapsed: bool
    labels: list[str]
    checked: bool
    is_deleted: bool
    added_at: str
    due: Due | None = None
    parent_id: int | None = None
    section_id: str | None = None
    day_order: int | None = None
    added_by_uid: str | None = None
    assigned_by_uid: str | None = None
    responsible_uid: str | None = None
    sync_id: str | None = None
    completed_at: str | None = None


@dataclass
class ItemCompletedInfo(DataClassJsonMixin):
    item_id: str
    completed_items: int


@dataclass
class CompletedItems(DataClassJsonMixin):
    items: list[Item]
    total: int
    completed_info: list[ItemCompletedInfo]
    has_more: bool
    next_cursor: str | None = None


@dataclass
class Duration(DataClassJsonMixin):
    amount: int
    unit: str
