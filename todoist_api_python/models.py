from typing import List, Optional

import attr


class Base(object):
    @classmethod
    def from_dict(cls, obj):
        return cls(**obj)

    @classmethod
    def from_item(cls, obj, key):
        val = obj.pop(key, None)
        if not val:
            return None
        return cls.from_dict(val)


@attr.s
class Project(Base):
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


@attr.s
class Section(Base):
    id: int = attr.ib()
    name: str = attr.ib()
    order: int = attr.ib()
    project_id: int = attr.ib()


@attr.s
class Due(Base):
    date: str = attr.ib()
    recurring: bool = attr.ib()
    string: str = attr.ib()
    datetime: Optional[str] = attr.ib(default=None)
    timezone: Optional[str] = attr.ib(default=None)


@attr.s
class Task(Base):
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
        due = Due.from_item(obj, "due")
        return cls(due=due, **obj)


@attr.s
class Collaborator(Base):
    id: int = attr.ib()
    email: str = attr.ib()
    name: str = attr.ib()
