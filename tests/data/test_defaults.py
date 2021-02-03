API_BASE_URL = "https://api.todoist.com/rest/v1"
DEFAULT_TOKEN = "A TOKEN"
DEFAULT_REQUEST_ID = "REQUEST12345"

DEFAULT_TASK_RESPONSE = {
    "id": 2995104339,
    "assigner": 2971358,
    "project_id": 2203306141,
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
}

DEFAULT_TASKS_RESPONSE = [
    DEFAULT_TASK_RESPONSE,
    DEFAULT_TASK_RESPONSE,
    DEFAULT_TASK_RESPONSE,
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
}

DEFAULT_PROJECTS_RESPONSE = [
    DEFAULT_PROJECT_RESPONSE,
    DEFAULT_PROJECT_RESPONSE,
    DEFAULT_PROJECT_RESPONSE,
]

DEFAULT_COLLABORATOR_RESPONSE = {"id": 1, "name": "Alice", "email": "alice@example.com"}

DEFAULT_COLLABORATORS_RESPONSE = [
    DEFAULT_COLLABORATOR_RESPONSE,
    DEFAULT_COLLABORATOR_RESPONSE,
    DEFAULT_COLLABORATOR_RESPONSE,
]

DEFAULT_SECTION_RESPONSE = {
    "id": 1234,
    "project_id": 4567,
    "name": "A Section",
    "order": 1,
}

DEFAULT_SECTIONS_RESPONSE = [
    DEFAULT_SECTION_RESPONSE,
    DEFAULT_SECTION_RESPONSE,
    DEFAULT_SECTION_RESPONSE,
]
