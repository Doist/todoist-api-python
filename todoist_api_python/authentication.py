from __future__ import annotations

from contextlib import asynccontextmanager, contextmanager
from typing import TYPE_CHECKING, Literal
from urllib.parse import urlencode

import httpx

if TYPE_CHECKING:
    from collections.abc import AsyncIterator, Iterator

from todoist_api_python._core.endpoints import (
    ACCESS_TOKEN_PATH,
    ACCESS_TOKENS_PATH,
    AUTHORIZE_PATH,
    get_api_url,
    get_oauth_url,
)
from todoist_api_python._core.http_requests import (
    delete,
    delete_async,
    post,
    post_async,
    response_json_dict,
)
from todoist_api_python.models import AuthResult

"""
Possible permission scopes:

- `data:read`: Read-only access
- `data:read_write`: Read and write access
- `data:delete`: Full access including delete
- `task:add`: Can create new tasks
- `project:delete`: Can delete projects
- `backups:read`: Can access user backups without MFA
"""
Scope = Literal[
    "task:add",
    "data:read",
    "data:read_write",
    "data:delete",
    "project:delete",
    "backups:read",
]


def get_authentication_url(client_id: str, scopes: list[Scope], state: str) -> str:
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
    client_id: str,
    client_secret: str,
    code: str,
    client: httpx.Client | None = None,
) -> AuthResult:
    """Get access token using provided client ID, client secret, and auth code."""
    endpoint = _get_access_token_url()
    data = _build_auth_token_data(client_id, client_secret, code)

    with _managed_client(client) as managed_client:
        response = post(
            client=managed_client,
            url=endpoint,
            data=data,
        )

    data = response_json_dict(response)
    return AuthResult.from_dict(data)


async def get_auth_token_async(
    client_id: str,
    client_secret: str,
    code: str,
    client: httpx.AsyncClient | None = None,
) -> AuthResult:
    """Get access token asynchronously."""
    endpoint = _get_access_token_url()
    data = _build_auth_token_data(client_id, client_secret, code)

    async with _managed_async_client(client) as managed_client:
        response = await post_async(
            client=managed_client,
            url=endpoint,
            data=data,
        )

    data = response_json_dict(response)
    return AuthResult.from_dict(data)


def revoke_auth_token(
    client_id: str,
    client_secret: str,
    token: str,
    client: httpx.Client | None = None,
) -> bool:
    """Revoke an access token."""
    endpoint = _get_access_tokens_url()
    params = _build_revoke_auth_token_params(client_id, client_secret, token)

    with _managed_client(client) as managed_client:
        response = delete(client=managed_client, url=endpoint, params=params)

    return response.is_success


async def revoke_auth_token_async(
    client_id: str,
    client_secret: str,
    token: str,
    client: httpx.AsyncClient | None = None,
) -> bool:
    """Revoke an access token asynchronously."""
    endpoint = _get_access_tokens_url()
    params = _build_revoke_auth_token_params(client_id, client_secret, token)

    async with _managed_async_client(client) as managed_client:
        response = await delete_async(
            client=managed_client, url=endpoint, params=params
        )

    return response.is_success


@contextmanager
def _managed_client(client: httpx.Client | None) -> Iterator[httpx.Client]:
    if client is not None:
        yield client
        return

    with httpx.Client() as default_client:
        yield default_client


@asynccontextmanager
async def _managed_async_client(
    client: httpx.AsyncClient | None,
) -> AsyncIterator[httpx.AsyncClient]:
    if client is not None:
        yield client
        return

    async with httpx.AsyncClient() as default_client:
        yield default_client


def _build_auth_token_data(
    client_id: str,
    client_secret: str,
    code: str,
) -> dict[str, str]:
    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
    }


def _build_revoke_auth_token_params(
    client_id: str,
    client_secret: str,
    token: str,
) -> dict[str, str]:
    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": token,
    }


def _get_access_token_url() -> str:
    return get_oauth_url(ACCESS_TOKEN_PATH)


def _get_access_tokens_url() -> str:
    # `get_api_url` is not a typo. Deleting access tokens is done using the regular API.
    return get_api_url(ACCESS_TOKENS_PATH)
