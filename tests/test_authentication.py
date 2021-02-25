import json
import urllib
from typing import Any, Dict

import pytest
import responses

from tests.data.test_defaults import AUTH_BASE_URL
from todoist_api_python.authentication import (
    get_auth_token,
    get_auth_token_async,
    get_authentication_url,
    revoke_auth_token,
    revoke_auth_token_async,
)
from todoist_api_python.endpoints import SYNC_API
from todoist_api_python.models import AuthResult


def test_get_authentication_url():
    client_id = "123"
    scopes = ["task:add", "data:read", "project:delete"]
    state = "456"
    params = (
        f"client_id={client_id}&scope={scopes[0]},{scopes[1]},{scopes[2]}&state={state}"
    )
    query = urllib.parse.quote(params, safe="=&")
    expected_url = f"{AUTH_BASE_URL}/oauth/authorize?{query}"

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


@pytest.mark.asyncio
async def test_revoke_auth_token(
    requests_mock: responses.RequestsMock,
):
    client_id = "123"
    client_secret = "456"
    token = "AToken"

    expected_payload = json.dumps(
        {"client_id": client_id, "client_secret": client_secret, "access_token": token}
    )

    requests_mock.add(
        responses.POST,
        f"{SYNC_API}access_tokens/revoke",
        status=204,
    )

    result = revoke_auth_token(client_id, client_secret, token)

    assert len(requests_mock.calls) == 1
    assert requests_mock.calls[0].request.body == expected_payload
    assert result is True

    result = await revoke_auth_token_async(client_id, client_secret, token)

    assert len(requests_mock.calls) == 2
    assert requests_mock.calls[1].request.body == expected_payload
    assert result is True
