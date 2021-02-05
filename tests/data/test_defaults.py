API_BASE_URL = "https://api.todoist.com/rest/v1"
DEFAULT_TOKEN = "A TOKEN"
DEFAULT_REQUEST_ID = "REQUEST12345"

DEFAULT_DUE_RESPONSE = {
    "date": "2016-09-01",
    "recurring": True,
    "datetime": "2016-09-01T09:00:00Z",
    "string": "tomorrow at 12",
    "timezone": "Europe/Moscow",
}

DEFAULT_TASK_RESPONSE = {
    "id": 1234,
    "assigner": 2971358,
    "assignee": 2423523,
    "project_id": 2203306141,
    "parent_id": 8686843758,
    "sync_id": 2345345346,
    "section_id": 7025,
    "order": 3,
    "content": "Some Task Content",
    "completed": False,
    "label_ids": [],
    "priority": 1,
    "comment_count": 0,
    "creator": 0,
    "created": "2019-01-02T21:00:30Z",
    "url": "https://todoist.com/showTask?id=2995104339",
    "due": DEFAULT_DUE_RESPONSE,
}

DEFAULT_TASK_RESPONSE_2 = dict(DEFAULT_TASK_RESPONSE)
DEFAULT_TASK_RESPONSE_2["id"] = 5678

DEFAULT_TASKS_RESPONSE = [
    DEFAULT_TASK_RESPONSE,
    DEFAULT_TASK_RESPONSE_2,
]

DEFAULT_PROJECT_RESPONSE = {
    "id": 1234,
    "name": "Inbox",
    "comment_count": 10,
    "order": 1,
    "color": 30,
    "shared": False,
    "parent_id": 5678,
    "sync_id": 0,
    "favorite": False,
    "inbox_project": True,
    "team_inbox": True,
}

DEFAULT_PROJECT_RESPONSE_2 = dict(DEFAULT_PROJECT_RESPONSE)
DEFAULT_PROJECT_RESPONSE_2["id"] = 5678

DEFAULT_PROJECTS_RESPONSE = [
    DEFAULT_PROJECT_RESPONSE,
    DEFAULT_PROJECT_RESPONSE_2,
]

DEFAULT_COLLABORATOR_RESPONSE = {
    "id": 1234,
    "name": "Alice",
    "email": "alice@example.com",
}

DEFAULT_COLLABORATOR_RESPONSE_2 = dict(DEFAULT_COLLABORATOR_RESPONSE)
DEFAULT_COLLABORATOR_RESPONSE_2["id"] = 5678

DEFAULT_COLLABORATORS_RESPONSE = [
    DEFAULT_COLLABORATOR_RESPONSE,
    DEFAULT_COLLABORATOR_RESPONSE_2,
]

DEFAULT_SECTION_RESPONSE = {
    "id": 1234,
    "project_id": 4567,
    "name": "A Section",
    "order": 1,
}

DEFAULT_SECTION_RESPONSE_2 = dict(DEFAULT_SECTION_RESPONSE)
DEFAULT_SECTION_RESPONSE_2["id"] = 5678

DEFAULT_SECTIONS_RESPONSE = [
    DEFAULT_SECTION_RESPONSE,
    DEFAULT_SECTION_RESPONSE_2,
]

DEFAULT_ATTACHMENT_RESPONSE = {
    "resource_type": "file",
    "file_name": "File.pdf",
    "file_type": "application/pdf",
    "file_size": 4321,
    "file_url": "https://cdn-domain.tld/path/to/file.pdf",
    "upload_state": "completed",
    "image": "https://cdn-domain.tld/path/to/some_image.jpg",
    "image_width": 1234,
    "image_height": 5678,
    "url": "https://todoist.com",
    "title": "Todoist Website",
}

DEFAULT_COMMENT_RESPONSE = {
    "id": 1234,
    "content": "A comment",
    "posted": "2016-09-22T07:00:00Z",
    "task_id": 2345,
    "project_id": 4567,
    "attachment": DEFAULT_ATTACHMENT_RESPONSE,
}

DEFAULT_COMMENT_RESPONSE_2 = dict(DEFAULT_COMMENT_RESPONSE)
DEFAULT_COMMENT_RESPONSE_2["id"] = 5678

DEFAULT_COMMENTS_RESPONSE = [
    DEFAULT_COMMENT_RESPONSE,
    DEFAULT_COMMENT_RESPONSE_2,
]

DEFAULT_LABEL_RESPONSE = {
    "id": 1234,
    "name": "A label",
    "color": 30,
    "order": 1,
    "favorite": True,
}

DEFAULT_LABEL_RESPONSE_2 = dict(DEFAULT_LABEL_RESPONSE)
DEFAULT_LABEL_RESPONSE_2["id"] = 4567

DEFAULT_LABELS_RESPONSE = [
    DEFAULT_LABEL_RESPONSE,
    DEFAULT_LABEL_RESPONSE_2,
]
