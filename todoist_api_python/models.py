from __future__ import annotations

from typing import Any, Dict, List, Literal

from pydantic import AliasChoices, BaseModel, Field, computed_field

from todoist_api_python.utils import get_url_for_task

VIEW_STYLE = Literal["list", "board"]


class Model(BaseModel, extra="allow"):
    @classmethod
    def from_dict(cls, obj: Dict[str, Any]):
        return cls(**obj)

    def to_dict(self) -> Dict[str, Any]:
        return self.model_dump()


class Project(Model):
    color: str
    comment_count: int
    id: str
    is_favorite: bool
    is_inbox_project: bool = False
    is_shared: bool
    is_team_inbox: bool = False
    name: str
    order: int = 0
    parent_id: str | None = None
    url: str
    view_style: VIEW_STYLE


class Section(Model):
    id: int | str
    name: str
    order: int
    project_id: str


class Due(Model):
    date: str
    is_recurring: bool
    string: str

    datetime: str | None = None
    timezone: str | None = None

    @classmethod
    def from_quick_add_response(cls, obj: Dict[str, Any]) -> Due | None:
        due = obj.get("due")

        if not due:
            return None

        timezone = due.get("timezone")
        datetime: str | None = due["date"] if timezone is not None else None

        due["datetime"] = datetime
        due["timezone"] = timezone

        return cls(**due)


class Task(Model):
    assignee_id: str | None = Field(
        validation_alias=AliasChoices("assignee_id", "responsible_uid")
    )
    assigner_id: str | None = Field(
        validation_alias=AliasChoices("assigner_id", "assigned_by_uid")
    )
    comment_count: int
    is_completed: bool
    content: str
    created_at: str = Field(validation_alias=AliasChoices("created_at", "added_at"))
    creator_id: str = Field(validation_alias=AliasChoices("creator_id", "added_by_uid"))
    description: str
    due: Due | None
    id: str
    labels: List[str]
    order: int = Field(validation_alias=AliasChoices("order", "child_order"))
    parent_id: str | None
    priority: int
    project_id: str
    section_id: str | None

    sync_id: str | None = None

    @computed_field  # type: ignore
    @property
    def url(self) -> str:
        return get_url_for_task(
            int(self.id), int(self.sync_id) if self.sync_id else None
        )

    @classmethod
    def from_quick_add_response(cls, obj: Dict[str, Any]) -> Task:
        obj_copy = obj.copy()
        obj_copy["due"] = (
            Due.from_quick_add_response(obj) if obj.get("due") is not None else None
        )
        obj_copy["comment_count"] = 0
        obj_copy["is_completed"] = False

        return cls(**obj_copy)


class QuickAddResult(Model):
    task: Task

    resolved_project_name: str | None = None
    resolved_assignee_name: str | None = None
    resolved_label_names: List[str] | None = None
    resolved_section_name: str | None = None

    @classmethod
    def from_quick_add_response(cls, obj: Dict[str, Any]) -> QuickAddResult:
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


class Collaborator(Model):
    id: str
    email: str
    name: str


class Attachment(Model):
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


class Comment(Model):
    attachment: Attachment | None = None
    content: str
    id: str
    posted_at: str
    project_id: str | None
    task_id: str | None


class Label(Model):
    id: str
    name: str
    color: str
    order: int
    is_favorite: bool


class AuthResult(Model):
    access_token: str
    state: str


class Item(Model):
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


class ItemCompletedInfo(Model):
    item_id: str
    completed_items: int


class CompletedItems(Model):
    items: list[Item]
    total: int
    completed_info: list[ItemCompletedInfo]
    has_more: bool
    next_cursor: str | None = None
