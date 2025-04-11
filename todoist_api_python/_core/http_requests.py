from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any, TypeVar, cast

from requests.status_codes import codes

from todoist_api_python._core.http_headers import create_headers

if TYPE_CHECKING:
    from requests import Session


# Timeouts for requests.
#
# 10 seconds for connecting is a recurring default and adheres to python-requests's
# recommendation of picking a value slightly larger than a multiple of 3.
#
# 60 seconds for reading aligns with Todoist's own internal timeout. All requests are
# forcefully terminated after this time, so there is no point waiting any longer.
TIMEOUT = (10, 60)

T = TypeVar("T")


def get(
    session: Session,
    url: str,
    token: str | None = None,
    params: dict[str, Any] | None = None,
) -> T:  # type: ignore[type-var]
    response = session.get(
        url, params=params, headers=create_headers(token=token), timeout=TIMEOUT
    )

    if response.status_code == codes.OK:
        return cast("T", response.json())

    response.raise_for_status()
    return cast("T", response.ok)


def post(
    session: Session,
    url: str,
    token: str | None = None,
    *,
    params: dict[str, Any] | None = None,
    data: dict[str, Any] | None = None,
) -> T:  # type: ignore[type-var]
    headers = create_headers(token=token, with_content=bool(data))

    response = session.post(
        url,
        headers=headers,
        data=json.dumps(data) if data else None,
        params=params,
        timeout=TIMEOUT,
    )

    if response.status_code == codes.OK:
        return cast("T", response.json())

    response.raise_for_status()
    return cast("T", response.ok)


def delete(
    session: Session,
    url: str,
    token: str | None = None,
    params: dict[str, Any] | None = None,
) -> bool:
    headers = create_headers(token=token)

    response = session.delete(url, params=params, headers=headers, timeout=TIMEOUT)

    response.raise_for_status()
    return response.ok
