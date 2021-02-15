import re
from typing import Callable, Optional

import pytest
import responses

from tests.data.test_defaults import DEFAULT_REQUEST_ID, DEFAULT_TOKEN
from todoist_api_python.api import TodoistAPI


def assert_auth_header(request):
    assert request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"


def assert_request_id_header(request):
    assert request.headers["X-Request-Id"] == DEFAULT_REQUEST_ID


def assert_id_validation(func: Callable, requests_mock: responses.RequestsMock):
    requests_mock.assert_all_requests_are_fired = False
    match_any_regex = re.compile(".*")

    requests_mock.add(responses.GET, match_any_regex)
    requests_mock.add(responses.POST, match_any_regex)
    requests_mock.add(responses.DELETE, match_any_regex)

    with pytest.raises(ValueError):
        func()

    assert len(requests_mock.calls) == 0


def get_todoist_api_patch(method: Optional[Callable]) -> str:
    module = TodoistAPI.__module__
    name = TodoistAPI.__qualname__

    return f"{module}.{name}.{method.__name__}" if method else f"{module}.{name}"
