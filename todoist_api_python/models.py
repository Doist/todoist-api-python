from typing import List, Optional

import attr

from todoist_api_python.utils import get_url_for_task


@attr.s
class Project(object):
    id: int = attr.ib()
    color: int = attr.ib()
    comment_count: int = attr.ib()
    favorite: bool = attr.ib()
    name: str = attr.ib()
    shared: bool = attr.ib()
    sync_id: int = attr.ib()
    url: str = attr.ib()

    inbox_project: Optional[bool] = attr.ib(default=None)
    team_inbox: Optional[bool] = attr.ib(default=None)
    order: Optional[int] = attr.ib(default=None)
    parent_id: Optional[int] = attr.ib(default=None)

    @classmethod
    def from_dict(cls, obj):
        return cls(
            id=obj["id"],
            color=obj["color"],
            comment_count=obj["comment_count"],
            favorite=obj["favorite"],
            name=obj["name"],
            shared=obj["shared"],
            sync_id=obj["sync_id"],
            url=obj["url"],
            inbox_project=obj.get("inbox_project"),
            team_inbox=obj.get("team_inbox"),
            order=obj.get("order"),
            parent_id=obj.get("parent_id"),
        )


@attr.s
class Section(object):
    id: int = attr.ib()
    name: str = attr.ib()
    order: int = attr.ib()
    project_id: int = attr.ib()

    @classmethod
    def from_dict(cls, obj):
        return cls(
            id=obj["id"],
            name=obj["name"],
            order=obj["order"],
            project_id=obj["project_id"],
        )


@attr.s
class Due(object):
    date: str = attr.ib()
    recurring: bool = attr.ib()
    string: str = attr.ib()
    datetime: Optional[str] = attr.ib(default=None)
    timezone: Optional[str] = attr.ib(default=None)

    @classmethod
    def from_dict(cls, obj):
        return cls(
            date=obj["date"],
            recurring=obj["recurring"],
            string=obj["string"],
            datetime=obj.get("datetime"),
            timezone=obj.get("timezone"),
        )

    def to_dict(self):
        return {
            "date": self.date,
            "recurring": self.recurring,
            "string": self.string,
            "datetime": self.datetime,
            "timezone": self.timezone,
        }

    @classmethod
    def from_quick_add_response(cls, obj):
        due = obj.get("due")

        if not due:
            return None

        timezone = due.get("timezone")

        datetime: Optional[str] = None

        if timezone:
            datetime = due["date"]

        return cls(
            date=due["date"],
            recurring=due["is_recurring"],
            string=due["string"],
            datetime=datetime,
            timezone=timezone,
        )


@attr.s
class Task(object):
    comment_count: int = attr.ib()
    completed: bool = attr.ib()
    content: str = attr.ib()
    created: str = attr.ib()
    creator: int = attr.ib()
    description: str = attr.ib()
    id: int = attr.ib()
    project_id: int = attr.ib()
    section_id: int = attr.ib()
    priority: int = attr.ib()
    url: str = attr.ib()

    assignee: Optional[int] = attr.ib(default=None)
    assigner: Optional[int] = attr.ib(default=None)
    due: Optional[Due] = attr.ib(default=None)
    label_ids: Optional[List[int]] = attr.ib(default=None)
    order: Optional[int] = attr.ib(default=None)
    parent_id: Optional[int] = attr.ib(default=None)
    sync_id: Optional[int] = attr.ib(default=None)

    @classmethod
    def from_dict(cls, obj):
        due: Optional[Due] = None

        if obj.get("due"):
            due = Due.from_dict(obj["due"])

        return cls(
            comment_count=obj["comment_count"],
            completed=obj["completed"],
            content=obj["content"],
            created=obj["created"],
            creator=obj["creator"],
            description=obj["description"],
            id=obj["id"],
            project_id=obj["project_id"],
            section_id=obj["section_id"],
            priority=obj["priority"],
            url=obj["url"],
            assignee=obj.get("assignee"),
            assigner=obj.get("assigner"),
            label_ids=obj.get("label_ids"),
            order=obj.get("order"),
            parent_id=obj.get("parent_id"),
            sync_id=obj.get("sync_id"),
            due=due,
        )

    def to_dict(self):
        due: Optional[dict] = None

        if self.due:
            due = self.due.to_dict()

        return {
            "comment_count": self.comment_count,
            "completed": self.completed,
            "content": self.content,
            "created": self.created,
            "creator": self.creator,
            "description": self.description,
            "id": self.id,
            "project_id": self.project_id,
            "section_id": self.section_id,
            "priority": self.priority,
            "url": self.url,
            "assignee": self.assignee,
            "assigner": self.assigner,
            "label_ids": self.label_ids,
            "order": self.order,
            "parent_id": self.parent_id,
            "sync_id": self.sync_id,
            "due": due,
        }

    @classmethod
    def from_quick_add_response(cls, obj):
        due: Optional[Due] = None

        if obj.get("due"):
            due = Due.from_quick_add_response(obj)

        return cls(
            comment_count=0,
            completed=False,
            content=obj["content"],
            created=obj["date_added"],
            creator=obj["added_by_uid"],
            description=obj["description"],
            id=obj["id"],
            project_id=obj["project_id"],
            section_id=obj["section_id"] or 0,
            priority=obj["priority"],
            url=get_url_for_task(obj["id"], obj["sync_id"]),
            assignee=obj.get("responsible_uid"),
            assigner=obj.get("assigned_by_uid"),
            label_ids=obj["labels"],
            order=obj["child_order"],
            parent_id=obj["parent_id"] or 0,
            sync_id=obj.get("sync_id"),
            due=due,
        )


@attr.s
class QuickAddResult:
    task: Task = attr.ib()

    resolved_project_name: Optional[str] = attr.ib(default=None)
    resolved_assignee_name: Optional[str] = attr.ib(default=None)
    resolved_label_names: Optional[List[str]] = attr.ib(default=None)
    resolved_section_name: Optional[str] = attr.ib(default=None)

    @classmethod
    def from_quick_add_response(cls, obj):
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

        return cls(
            task=Task.from_quick_add_response(obj),
            resolved_project_name=resolved_project_name,
            resolved_assignee_name=resolved_assignee_name,
            resolved_label_names=list(obj["meta"]["labels"].values()),
            resolved_section_name=resolved_section_name,
        )


@attr.s
class Collaborator(object):
    id: int = attr.ib()
    email: str = attr.ib()
    name: str = attr.ib()

    @classmethod
    def from_dict(cls, obj):
        return cls(
            id=obj["id"],
            email=obj["email"],
            name=obj["name"],
        )


@attr.s
class Attachment(object):
    resource_type: Optional[str] = attr.ib(default=None)

    file_name: Optional[str] = attr.ib(default=None)
    file_size: Optional[int] = attr.ib(default=None)
    file_type: Optional[str] = attr.ib(default=None)
    file_url: Optional[str] = attr.ib(default=None)
    file_duration: Optional[int] = attr.ib(default=None)
    upload_state: Optional[str] = attr.ib(default=None)

    image: Optional[str] = attr.ib(default=None)
    image_width: Optional[int] = attr.ib(default=None)
    image_height: Optional[int] = attr.ib(default=None)

    url: Optional[str] = attr.ib(default=None)
    title: Optional[str] = attr.ib(default=None)

    @classmethod
    def from_dict(cls, obj):
        return cls(
            resource_type=obj.get("resource_type"),
            file_name=obj.get("file_name"),
            file_size=obj.get("file_size"),
            file_type=obj.get("file_type"),
            file_url=obj.get("file_url"),
            upload_state=obj.get("upload_state"),
            image=obj.get("image"),
            image_width=obj.get("image_width"),
            image_height=obj.get("image_height"),
            url=obj.get("url"),
            title=obj.get("title"),
        )


@attr.s
class Comment(object):
    id: int = attr.ib()
    content: str = attr.ib()
    posted: str = attr.ib()

    task_id: Optional[int] = attr.ib(default=None)
    project_id: Optional[int] = attr.ib(default=None)
    attachment: Optional[Attachment] = attr.ib(default=None)

    @classmethod
    def from_dict(cls, obj):
        attachment: Optional[Attachment] = None

        if "attachment" in obj:
            attachment = Attachment.from_dict(obj["attachment"])

        return cls(
            id=obj["id"],
            content=obj["content"],
            posted=obj["posted"],
            task_id=obj.get("task_id"),
            project_id=obj.get("project_id"),
            attachment=attachment,
        )


@attr.s
class Label:
    id: int = attr.ib()
    name: str = attr.ib()
    color: int = attr.ib()
    order: int = attr.ib()
    favorite: bool = attr.ib()

    @classmethod
    def from_dict(cls, obj):
        return cls(
            id=obj["id"],
            name=obj["name"],
            color=obj["color"],
            order=obj["order"],
            favorite=obj["favorite"],
        )


@attr.s
class AuthResult:
    access_token: str = attr.ib()
    state: str = attr.ib()

    @classmethod
    def from_dict(cls, obj):
        return cls(
            access_token=obj["access_token"],
            state=obj["state"],
        )
