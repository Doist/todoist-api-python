from __future__ import annotations

from typing import Any
from urllib.parse import urlencode

import requests
from requests import Session

from todoist_api_python._core.endpoints import (
    ACCESS_TOKEN_PATH,
    ACCESS_TOKENS_PATH,
    AUTHORIZE_PATH,
    get_api_url,
    get_oauth_url,
)
from todoist_api_python._core.http_requests import delete, post
from todoist_api_python._core.utils import run_async
from todoist_api_python.models import AuthResult


def get_authentication_url(client_id: str, scopes: list[str], state: str) -> str:
    """Get authorization URL to initiate OAuth flow."""
    if len(scopes) == 0:
        raise ValueError("At least one authorization scope should be requested.")

    endpoint = get_oauth_url(AUTHORIZE_PATH)
    query = {
        "client_id": client_id,
        "scope": ",".join(scopes),
        "state": state,
    }
    return f"{endpoint}?{urlencode(query)}"


def get_auth_token(
    client_id: str, client_secret: str, code: str, session: Session | None = None
) -> AuthResult:
    """Get access token using provided client ID, client secret, and auth code."""
    endpoint = get_oauth_url(ACCESS_TOKEN_PATH)
    session = session or requests.Session()
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }
    response: dict[str, Any] = post(session=session, url=endpoint, data=data)
    return AuthResult.from_dict(response)


async def get_auth_token_async(
    client_id: str, client_secret: str, code: str
) -> AuthResult:
    return await run_async(lambda: get_auth_token(client_id, client_secret, code))


def revoke_auth_token(
    client_id: str, client_secret: str, token: str, session: Session | None = None
) -> bool:
    """Revoke an access token."""
    # `get_api_url` is not a typo. Deleting access tokens is done using the regular API.
    endpoint = get_api_url(ACCESS_TOKENS_PATH)
    session = session or requests.Session()
    params = {
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": token,
    }
    return delete(session=session, url=endpoint, params=params)


async def revoke_auth_token_async(
    client_id: str, client_secret: str, token: str
) -> bool:
    return await run_async(lambda: revoke_auth_token(client_id, client_secret, token))
