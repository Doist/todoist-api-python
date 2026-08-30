from __future__ import annotations

from typing import TYPE_CHECKING, Any
from urllib.parse import quote

import pytest

from tests.data.test_defaults import DEFAULT_OAUTH_URL
from tests.utils.test_utils import mock_route
from todoist_api_python._core.endpoints import API_URL  # Use new base URL
from todoist_api_python.authentication import (
    get_auth_token,
    get_auth_token_async,
    get_authentication_url,
    revoke_auth_token,
    revoke_auth_token_async,
)

if TYPE_CHECKING:
    import respx

    from todoist_api_python.authentication import Scope
    from todoist_api_python.models import AuthResult


def test_get_authentication_url() -> None:
    client_id = "123"
    scopes: list[Scope] = ["task:add", "data:read", "project:delete"]
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
    respx_mock: respx.MockRouter,
    default_auth_response: dict[str, Any],
    default_auth_result: AuthResult,
) -> None:
    client_id = "123"
    client_secret = "456"
    code = "789"

    mock_route(
        respx_mock,
        "POST",
        f"{DEFAULT_OAUTH_URL}/access_token",
        request_json={
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
        },
        response_json=default_auth_response,
        response_status=200,
    )

    auth_result = get_auth_token(client_id, client_secret, code)

    assert len(respx_mock.calls) == 1
    assert auth_result == default_auth_result

    auth_result = await get_auth_token_async(client_id, client_secret, code)

    assert len(respx_mock.calls) == 2
    assert auth_result == default_auth_result


@pytest.mark.asyncio
async def test_revoke_auth_token(
    respx_mock: respx.MockRouter,
) -> None:
    client_id = "123"
    client_secret = "456"
    token = "AToken"

    mock_route(
        respx_mock,
        "DELETE",
        f"{API_URL}/access_tokens",
        request_params={
            "client_id": client_id,
            "client_secret": client_secret,
            "access_token": token,
        },
        response_status=200,
    )

    result = revoke_auth_token(client_id, client_secret, token)

    assert len(respx_mock.calls) == 1
    assert result is True

    result = await revoke_auth_token_async(client_id, client_secret, token)

    assert len(respx_mock.calls) == 2
    assert result is True
