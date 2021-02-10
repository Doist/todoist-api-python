import json
from typing import Any, Dict

import pytest
import responses

from tests.data.test_defaults import AUTH_BASE_URL
from todoist_api_python.authentication import (
    get_auth_token,
    get_auth_token_async,
    get_authentication_url,
)
from todoist_api_python.models import AuthResult


def test_get_authentication_url():
    client_id = "123"
    scopes = ["task:add", "data:read", "project:delete"]
    state = "456"
    expected_url = (
        f"{AUTH_BASE_URL}/oauth/authorize?"
        f"client_id={client_id}&scope={scopes[0]},{scopes[1]},{scopes[2]}&state={state}"
    )

    url = get_authentication_url(client_id, scopes, state)

    assert url == expected_url


@pytest.mark.asyncio
async def test_get_auth_token(
    requests_mock: responses.RequestsMock,
    default_auth_response: Dict[str, Any],
    default_auth_result: AuthResult,
):
    client_id = "123"
    client_secret = "456"
    code = "789"

    expected_payload = json.dumps(
        {"client_id": client_id, "client_secret": client_secret, "code": code}
    )

    requests_mock.add(
        responses.POST,
        f"{AUTH_BASE_URL}/oauth/access_token",
        json=default_auth_response,
        status=200,
    )

    auth_result = get_auth_token(client_id, client_secret, code)

    assert len(requests_mock.calls) == 1
    assert requests_mock.calls[0].request.body == expected_payload
    assert auth_result == default_auth_result

    auth_result = await get_auth_token_async(client_id, client_secret, code)

    assert len(requests_mock.calls) == 2
    assert requests_mock.calls[1].request.body == expected_payload
    assert auth_result == default_auth_result
