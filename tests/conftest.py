import pytest

from todoist_api_python import TodoistAPI

DEFAULT_TOKEN = "A TOKEN"


@pytest.fixture()
def todoist_api() -> TodoistAPI:
    return TodoistAPI(DEFAULT_TOKEN)
