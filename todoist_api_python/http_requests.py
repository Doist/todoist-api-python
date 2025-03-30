from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

from requests.status_codes import codes

from todoist_api_python.headers import create_headers

if TYPE_CHECKING:
    from requests import Session

    Json = dict[str, "Json"] | list["Json"] | str | int | float | bool | None


def get(
    session: Session,
    url: str,
    token: str | None = None,
    params: dict[str, Any] | None = None,
) -> Json | bool:
    response = session.get(url, params=params, headers=create_headers(token=token))

    if response.status_code == codes.OK:
        return response.json()

    response.raise_for_status()
    return response.ok


def post(
    session: Session,
    url: str,
    token: str | None = None,
    data: dict[str, Any] | None = None,
) -> Json | bool:
    request_id = data.pop("request_id", None) if data else None

    headers = create_headers(
        token=token, with_content=bool(data), request_id=request_id
    )

    response = session.post(
        url,
        headers=headers,
        data=json.dumps(data) if data else None,
    )

    if response.status_code == codes.OK:
        return response.json()

    response.raise_for_status()
    return response.ok


def delete(
    session: Session,
    url: str,
    token: str | None = None,
    args: dict[str, Any] | None = None,
) -> bool:
    request_id = args.pop("request_id", None) if args else None

    headers = create_headers(token=token, request_id=request_id)

    response = session.delete(
        url,
        headers=headers,
    )

    response.raise_for_status()
    return response.ok
