from typing import List, Optional

import attr


@attr.s
class Project(object):
    id: int = attr.ib()
    color: int = attr.ib()
    comment_count: int = attr.ib()
    favorite: bool = attr.ib()
    name: str = attr.ib()
    shared: bool = attr.ib()
    sync_id: int = attr.ib()

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


@attr.s
class Task(object):
    comment_count: int = attr.ib()
    completed: bool = attr.ib()
    content: str = attr.ib()
    created: str = attr.ib()
    creator: int = attr.ib()
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
        return cls(
            comment_count=obj["comment_count"],
            completed=obj["completed"],
            content=obj["content"],
            created=obj["created"],
            creator=obj["creator"],
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
            due=Due.from_dict(obj["due"]) if "due" in obj else None,
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
    resource_type: str = attr.ib()

    file_name: Optional[str] = attr.ib(default=None)
    file_size: Optional[int] = attr.ib(default=None)
    file_type: Optional[str] = attr.ib(default=None)
    file_url: Optional[str] = attr.ib(default=None)
    upload_state: Optional[str] = attr.ib(default=None)

    image: Optional[str] = attr.ib(default=None)
    image_width: Optional[int] = attr.ib(default=None)
    image_height: Optional[int] = attr.ib(default=None)

    url: Optional[str] = attr.ib(default=None)
    title: Optional[str] = attr.ib(default=None)

    @classmethod
    def from_dict(cls, obj):
        return cls(
            resource_type=obj["resource_type"],
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
        return cls(
            id=obj["id"],
            content=obj["content"],
            posted=obj["posted"],
            task_id=obj.get("task_id"),
            project_id=obj.get("project_id"),
            attachment=Attachment.from_dict(obj["attachment"])
            if "attachment" in obj
            else None,
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
            order=obj.get("order"),
            favorite=obj.get("favorite"),
        )
