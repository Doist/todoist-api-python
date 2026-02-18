from __future__ import annotations

from typing import Any, TypedDict


class PaginatedResults(TypedDict):
    results: list[dict[str, Any]]
    next_cursor: str | None


class PaginatedItems(TypedDict):
    items: list[dict[str, Any]]
    next_cursor: str | None


DEFAULT_API_URL = "https://api.todoist.com/api/v1"
DEFAULT_OAUTH_URL = "https://todoist.com/oauth"

DEFAULT_TOKEN = "some-default-token"

DEFAULT_REQUEST_ID = "f00dbeef-cafe-4bad-a555-deadc0decafe"

DEFAULT_DUE_RESPONSE = {
    "date": "2016-09-01",
    "timezone": "Europe/Moscow",
    "string": "tomorrow at 12",
    "lang": "en",
    "is_recurring": True,
}

DEFAULT_DEADLINE_RESPONSE = {
    "date": "2016-09-01",
    "lang": "en",
}

DEFAULT_DURATION_RESPONSE = {
    "amount": 60,
    "unit": "minute",
}

DEFAULT_META_RESPONSE: dict[str, Any] = {
    "project": ["6X7rM8997g3RQmvh", "Inbox"],
    "section": [None, None],
    "assignee": [None, None],
    "labels": {},
    "due": None,
    "deadline": None,
}

DEFAULT_PROJECT_RESPONSE = {
    "id": "6X7rM8997g3RQmvh",
    "name": "Inbox",
    "description": "",
    "parent_id": "6X7rfFVPjhvv84XG",
    "folder_id": None,
    "workspace_id": None,
    "child_order": 1,
    "color": "red",
    "shared": False,
    "collapsed": False,
    "is_favorite": False,
    "is_inbox_project": True,
    "can_assign_tasks": False,
    "is_archived": False,
    "view_style": "list",
    "created_at": "2023-02-01T00:00:00.000000Z",
    "updated_at": "2025-04-03T03:14:15.926536Z",
}

DEFAULT_PROJECT_RESPONSE_2 = dict(DEFAULT_PROJECT_RESPONSE)
DEFAULT_PROJECT_RESPONSE_2["id"] = "6X7rfFVPjhvv84XG"
DEFAULT_PROJECT_RESPONSE_2["is_inbox_project"] = False


DEFAULT_PROJECT_RESPONSE_3 = dict(DEFAULT_PROJECT_RESPONSE)
DEFAULT_PROJECT_RESPONSE_3["id"] = "6X7rfEVP8hvv25ZQ"
DEFAULT_PROJECT_RESPONSE_3["is_inbox_project"] = False

DEFAULT_PROJECTS_RESPONSE: list[PaginatedResults] = [
    {
        "results": [DEFAULT_PROJECT_RESPONSE, DEFAULT_PROJECT_RESPONSE_2],
        "next_cursor": "next",
    },
    {
        "results": [DEFAULT_PROJECT_RESPONSE_3],
        "next_cursor": None,
    },
]

DEFAULT_TASK_RESPONSE: dict[str, Any] = {
    "id": "6X7rM8997g3RQmvh",
    "content": "Some task content",
    "description": "Some task description",
    "project_id": "6Jf8VQXxpwv56VQ7",
    "section_id": "3Ty8VQXxpwv28PK3",
    "parent_id": "6X7rf9x6pv2FGghW",
    "labels": [],
    "priority": 1,
    "due": DEFAULT_DUE_RESPONSE,
    "deadline": DEFAULT_DEADLINE_RESPONSE,
    "duration": DEFAULT_DURATION_RESPONSE,
    "collapsed": False,
    "child_order": 3,
    "responsible_uid": "2423523",
    "assigned_by_uid": "2971358",
    "completed_at": None,
    "added_by_uid": "34567",
    "added_at": "2014-09-26T08:25:05.000000Z",
    "updated_at": "2016-01-02T21:00:30.000000Z",
}

DEFAULT_TASK_RESPONSE_2 = dict(DEFAULT_TASK_RESPONSE)
DEFAULT_TASK_RESPONSE_2["id"] = "6X7rfFVPjhvv84XG"

DEFAULT_TASK_RESPONSE_3 = dict(DEFAULT_TASK_RESPONSE)
DEFAULT_TASK_RESPONSE_3["id"] = "6X7rF9xvX25jTxm5"

DEFAULT_TASKS_RESPONSE: list[PaginatedResults] = [
    {
        "results": [DEFAULT_TASK_RESPONSE, DEFAULT_TASK_RESPONSE_2],
        "next_cursor": "next",
    },
    {
        "results": [DEFAULT_TASK_RESPONSE_3],
        "next_cursor": None,
    },
]

DEFAULT_TASK_META_RESPONSE = dict(DEFAULT_TASK_RESPONSE)
DEFAULT_TASK_META_RESPONSE["meta"] = DEFAULT_META_RESPONSE

DEFAULT_COMPLETED_TASK_RESPONSE = dict(DEFAULT_TASK_RESPONSE)
DEFAULT_COMPLETED_TASK_RESPONSE["completed_at"] = "2024-02-13T10:00:00.000000Z"

DEFAULT_COMPLETED_TASK_RESPONSE_2 = dict(DEFAULT_COMPLETED_TASK_RESPONSE)
DEFAULT_COMPLETED_TASK_RESPONSE_2["id"] = "6X7rfFVPjhvv84XG"

DEFAULT_COMPLETED_TASK_RESPONSE_3 = dict(DEFAULT_COMPLETED_TASK_RESPONSE)
DEFAULT_COMPLETED_TASK_RESPONSE_3["id"] = "6X7rfEVP8hvv25ZQ"

DEFAULT_COMPLETED_TASKS_RESPONSE: list[PaginatedItems] = [
    {
        "items": [
            DEFAULT_COMPLETED_TASK_RESPONSE,
            DEFAULT_COMPLETED_TASK_RESPONSE_2,
        ],
        "next_cursor": "next",
    },
    {
        "items": [DEFAULT_COMPLETED_TASK_RESPONSE_3],
        "next_cursor": None,
    },
]

DEFAULT_COLLABORATOR_RESPONSE = {
    "id": "6X7rM8997g3RQmvh",
    "name": "Alice",
    "email": "alice@example.com",
}

DEFAULT_COLLABORATOR_RESPONSE_2 = dict(DEFAULT_COLLABORATOR_RESPONSE)
DEFAULT_COLLABORATOR_RESPONSE_2["id"] = "6X7rfFVPjhvv84XG"

DEFAULT_COLLABORATOR_RESPONSE_3 = dict(DEFAULT_COLLABORATOR_RESPONSE)
DEFAULT_COLLABORATOR_RESPONSE_3["id"] = "6X7rjKtP98vG84rK"

DEFAULT_COLLABORATORS_RESPONSE: list[PaginatedResults] = [
    {
        "results": [DEFAULT_COLLABORATOR_RESPONSE, DEFAULT_COLLABORATOR_RESPONSE_2],
        "next_cursor": "next",
    },
    {
        "results": [DEFAULT_COLLABORATOR_RESPONSE_3],
        "next_cursor": None,
    },
]

DEFAULT_SECTION_RESPONSE = {
    "id": "6X7rM8997g3RQmvh",
    "project_id": "4567",
    "name": "A Section",
    "collapsed": False,
    "order": 1,
}

DEFAULT_SECTION_RESPONSE_2 = dict(DEFAULT_SECTION_RESPONSE)
DEFAULT_SECTION_RESPONSE_2["id"] = "6X7FxXvX84jHphx"

DEFAULT_SECTION_RESPONSE_3 = dict(DEFAULT_SECTION_RESPONSE)
DEFAULT_SECTION_RESPONSE_3["id"] = "6X7rF9xvX25jTzm7"

DEFAULT_SECTIONS_RESPONSE: list[PaginatedResults] = [
    {
        "results": [DEFAULT_SECTION_RESPONSE, DEFAULT_SECTION_RESPONSE_2],
        "next_cursor": "next",
    },
    {
        "results": [DEFAULT_SECTION_RESPONSE_3],
        "next_cursor": None,
    },
]

DEFAULT_ATTACHMENT_RESPONSE = {
    "resource_type": "file",
    "file_name": "File.pdf",
    "file_type": "application/pdf",
    "file_size": 4321,
    "file_url": "https://cdn-domain.tld/path/to/file.pdf",
    "upload_state": "completed",
    "image": "https://cdn-domain.tld/path/to/some_image.jpg",
    "image_width": 800,
    "image_height": 600,
    "url": "https://todoist.com",
    "title": "Todoist Website",
}

DEFAULT_COMMENT_RESPONSE: dict[str, Any] = {
    "id": "6X7rM8997g3RQmvh",
    "content": "A comment",
    "posted_uid": "34567",
    "posted_at": "2019-09-22T07:00:00.000000Z",
    "task_id": "6X7rM8997g3RQmvh",
    "project_id": "6X7rfEVP8hvv25ZQ",
    "attachment": DEFAULT_ATTACHMENT_RESPONSE,
}

DEFAULT_COMMENT_RESPONSE_2 = dict(DEFAULT_COMMENT_RESPONSE)
DEFAULT_COMMENT_RESPONSE_2["id"] = "6X7rfFVPjhvv84XG"
DEFAULT_COMMENT_RESPONSE_2["attachment"] = None

DEFAULT_COMMENT_RESPONSE_3 = dict(DEFAULT_COMMENT_RESPONSE)
DEFAULT_COMMENT_RESPONSE_3["id"] = "6X7rfFVPjhvv65HG"
DEFAULT_COMMENT_RESPONSE_3["attachment"] = None

DEFAULT_COMMENTS_RESPONSE: list[PaginatedResults] = [
    {
        "results": [DEFAULT_COMMENT_RESPONSE, DEFAULT_COMMENT_RESPONSE_2],
        "next_cursor": "next",
    },
    {
        "results": [DEFAULT_COMMENT_RESPONSE_3],
        "next_cursor": None,
    },
]

DEFAULT_LABEL_RESPONSE = {
    "id": "1234",
    "name": "A label",
    "color": "red",
    "order": 1,
    "is_favorite": True,
}

DEFAULT_LABEL_RESPONSE_2 = dict(DEFAULT_LABEL_RESPONSE)
DEFAULT_LABEL_RESPONSE_2["id"] = "4567"

DEFAULT_LABEL_RESPONSE_3 = dict(DEFAULT_LABEL_RESPONSE)
DEFAULT_LABEL_RESPONSE_3["id"] = "6789"

DEFAULT_LABELS_RESPONSE: list[PaginatedResults] = [
    {
        "results": [DEFAULT_LABEL_RESPONSE, DEFAULT_LABEL_RESPONSE_2],
        "next_cursor": "next",
    },
    {
        "results": [DEFAULT_LABEL_RESPONSE_3],
        "next_cursor": None,
    },
]

DEFAULT_FOLDER_RESPONSE = {
    "id": "6X7rM8997g3RQmvh",
    "name": "Test Folder",
    "workspace_id": "ws_001",
    "default_order": 1,
    "child_order": 1,
    "is_deleted": False,
}

DEFAULT_FOLDER_RESPONSE_2 = dict(DEFAULT_FOLDER_RESPONSE)
DEFAULT_FOLDER_RESPONSE_2["id"] = "6X7rfFVPjhvv84XG"

DEFAULT_FOLDER_RESPONSE_3 = dict(DEFAULT_FOLDER_RESPONSE)
DEFAULT_FOLDER_RESPONSE_3["id"] = "6X7rfEVP8hvv25ZQ"

DEFAULT_FOLDERS_RESPONSE: list[PaginatedResults] = [
    {
        "results": [DEFAULT_FOLDER_RESPONSE, DEFAULT_FOLDER_RESPONSE_2],
        "next_cursor": "next",
    },
    {
        "results": [DEFAULT_FOLDER_RESPONSE_3],
        "next_cursor": None,
    },
]

DEFAULT_AUTH_RESPONSE = {
    "access_token": "123456789",
    "state": "somestate",
}
