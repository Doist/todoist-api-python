from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

import pytest
import responses

from tests.data.test_defaults import DEFAULT_OAUTH_URL
from tests.utils.test_utils import data_matcher, param_matcher
from todoist_api_python._core.endpoints import API_URL  # Use new base URL
from todoist_api_python.authentication import (
    get_auth_token,
    get_auth_token_async,
    get_authentication_url,
    revoke_auth_token,
    revoke_auth_token_async,
)

if TYPE_CHECKING:
    from todoist_api_python.models import AuthResult


def test_get_authentication_url() -> None:
    client_id = "123"
    scopes = ["task:add", "data:read", "project:delete"]
    state = "456"
    params = (
        f"client_id={client_id}&scope={scopes[0]},{scopes[1]},{scopes[2]}&state={state}"
    )
    query = quote(params, safe="=&")
    expected_url = f"{DEFAULT_OAUTH_URL}/authorize?{query}"

    url = get_authentication_url(client_id, scopes, state)

    assert url == expected_url


@pytest.mark.asyncio
async def test_get_auth_token(
    requests_mock: responses.RequestsMock,
    default_auth_response: dict[str, Any],
    default_auth_result: AuthResult,
) -> None:
    client_id = "123"
    client_secret = "456"
    code = "789"

    requests_mock.add(
        responses.POST,
        f"{DEFAULT_OAUTH_URL}/access_token",
        json=default_auth_response,
        status=200,
        match=[
            data_matcher(
                {"client_id": client_id, "client_secret": client_secret, "code": code}
            )
        ],
    )

    auth_result = get_auth_token(client_id, client_secret, code)

    assert len(requests_mock.calls) == 1
    assert auth_result == default_auth_result

    auth_result = await get_auth_token_async(client_id, client_secret, code)

    assert len(requests_mock.calls) == 2
    assert auth_result == default_auth_result


@pytest.mark.asyncio
async def test_revoke_auth_token(
    requests_mock: responses.RequestsMock,
) -> None:
    client_id = "123"
    client_secret = "456"
    token = "AToken"

    requests_mock.add(
        responses.DELETE,
        f"{API_URL}/access_tokens",
        match=[
            param_matcher(
                {
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "access_token": token,
                }
            )
        ],
        status=200,
    )

    result = revoke_auth_token(client_id, client_secret, token)

    assert len(requests_mock.calls) == 1
    assert result is True

    result = await revoke_auth_token_async(client_id, client_secret, token)

    assert len(requests_mock.calls) == 2
    assert result is True
