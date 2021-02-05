from urllib.parse import urljoin

BASE_URL = "https://api.todoist.com"
SYNC_VERSION = "v8"
REST_VERSION = "v1"

SYNC_API = urljoin(BASE_URL, "/sync/%s/" % SYNC_VERSION)
REST_API = urljoin(BASE_URL, "/rest/%s/" % REST_VERSION)

TASKS_ENDPOINT = "tasks"
PROJECTS_ENDPOINT = "projects"
COLLABORATORS_ENDPOINT = "collaborators"
SECTIONS_ENDPOINT = "sections"
COMMENTS_ENDPOINT = "comments"
LABELS_ENDPOINT = "labels"


def get_rest_url(relative_path: str) -> str:
    return urljoin(REST_API, relative_path)
