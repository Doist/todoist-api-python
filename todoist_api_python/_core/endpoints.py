from __future__ import annotations

import re
import unicodedata

API_VERSION = "v1"

API_URL = f"https://api.todoist.com/api/{API_VERSION}"
OAUTH_URL = "https://todoist.com/oauth"
PROJECT_URL = "https://app.todoist.com/app/project"
INBOX_URL = "https://app.todoist.com/app/inbox"
TASK_URL = "https://app.todoist.com/app/task"

TASKS_PATH = "tasks"
TASKS_FILTER_PATH = "tasks/filter"
TASKS_QUICK_ADD_PATH = "tasks/quick"
PROJECTS_PATH = "projects"
COLLABORATORS_PATH = "collaborators"
SECTIONS_PATH = "sections"
COMMENTS_PATH = "comments"
LABELS_PATH = "labels"
SHARED_LABELS_PATH = "labels/shared"
SHARED_LABELS_RENAME_PATH = f"{SHARED_LABELS_PATH}/rename"
SHARED_LABELS_REMOVE_PATH = f"{SHARED_LABELS_PATH}/remove"

AUTHORIZE_PATH = "authorize"
ACCESS_TOKEN_PATH = "access_token"  # noqa: S105
ACCESS_TOKENS_PATH = "access_tokens"


def get_oauth_url(relative_path: str) -> str:
    """
    Generate the URL for a given OAuth endpoint.

    :param relative_path: The relative path of the endpoint.
    :return: The URL string for the OAuth endpoint.
    """
    return f"{OAUTH_URL}/{relative_path}"


def get_api_url(relative_path: str) -> str:
    """
    Generate the URL for a given API endpoint.

    :param relative_path: The relative path of the endpoint.
    :return: The URL string for the API endpoint.
    """
    return f"{API_URL}/{relative_path}"


def get_task_url(task_id: str, content: str | None = None) -> str:
    """
    Generate the URL for a given task.

    :param task_id: The ID of the task.
    :param content: The content of the task.
    :return: The URL string for the task view.
    """
    slug = _slugify(content) if content is not None else None
    path = f"{slug}-{task_id}" if content else task_id
    return f"{TASK_URL}/{path}"


def get_project_url(project_id: str, name: str | None = None) -> str:
    """
    Generate the URL for a given project.

    :param project_id: The ID of the project.
    :param name: The name of the project.
    :return: The URL string for the project view.
    """
    slug = _slugify(name) if name is not None else None
    path = f"{slug}-{project_id}" if name else project_id
    return f"{PROJECT_URL}/{path}"


def _slugify(value: str) -> str:
    """
    Slugify function borrowed from Django.

    Convert to ASCII. Convert spaces or repeated dashes to single dashes.
    Remove characters that aren't alphanumerics, underscores, or hyphens.
    Convert to lowercase. Strip spaces, dashes, and underscores.
    """
    value = (
        unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    )
    value = re.sub(r"[^\w\s-]", "", value.lower())
    return re.sub(r"[-\s]+", "-", value).strip("-_")
