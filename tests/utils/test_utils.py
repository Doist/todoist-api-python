from __future__ import annotations

import re
from typing import TYPE_CHECKING

from tests.data.test_defaults import DEFAULT_REQUEST_ID, DEFAULT_TOKEN
from todoist_api_python.api import TodoistAPI

if TYPE_CHECKING:
    from collections.abc import Callable

    from requests import Request

MATCH_ANY_REGEX = re.compile(".*")


def assert_auth_header(request: Request) -> None:
    assert request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"


def assert_request_id_header(request: Request) -> None:
    assert request.headers["X-Request-Id"] == DEFAULT_REQUEST_ID


def get_todoist_api_patch(method: Callable | None) -> str:
    module = TodoistAPI.__module__
    name = TodoistAPI.__qualname__

    return f"{module}.{name}.{method.__name__}" if method else f"{module}.{name}"
