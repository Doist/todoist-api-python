from typing import Callable, Optional

from tests.data.test_defaults import DEFAULT_REQUEST_ID, DEFAULT_TOKEN
from todoist_api_python.api import TodoistAPI


def assert_auth_header(request):
    assert request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"


def assert_request_id_header(request):
    assert request.headers["X-Request-Id"] == DEFAULT_REQUEST_ID


def get_todoist_api_patch(method: Optional[Callable]) -> str:
    module = TodoistAPI.__module__
    name = TodoistAPI.__qualname__

    return f"{module}.{name}.{method.__name__}" if method else f"{module}.{name}"
