from typing import List

from todoist.models import Task

DEFAULT_REQUEST_ID = "REQUEST12345"

DEFAULT_TASK_DATA = {
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

DEFAULT_PROJECT_DATA = {
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

DEFAULT_TASKS_DATA = [
    DEFAULT_TASK_DATA,
    DEFAULT_TASK_DATA,
    DEFAULT_TASK_DATA,
]

DEFAULT_TASK: Task = Task.from_dict(DEFAULT_TASK_DATA)
DEFAULT_TASKS_LIST: List[Task] = [Task.from_dict(obj) for obj in DEFAULT_TASKS_DATA]
