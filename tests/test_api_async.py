from unittest.mock import MagicMock, patch

import requests

from tests.data.test_defaults import DEFAULT_TOKEN
from tests.utils.test_utils import get_todoist_api_patch
from todoist_api_python.api import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync


@patch(get_todoist_api_patch(TodoistAPI.__init__))
def test_constructs_api_with_token(sync_api_constructor: MagicMock):
    sync_api_constructor.return_value = None
    TodoistAPIAsync(DEFAULT_TOKEN)

    sync_api_constructor.assert_called_once_with(DEFAULT_TOKEN, None)


@patch(get_todoist_api_patch(TodoistAPI.__init__))
def test_constructs_api_with_token_and_session(sync_api_constructor: MagicMock):
    sync_api_constructor.return_value = None
    s = requests.Session()
    TodoistAPIAsync(DEFAULT_TOKEN, s)
    sync_api_constructor.assert_called_once_with(DEFAULT_TOKEN, s)
