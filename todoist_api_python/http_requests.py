import json
from typing import Any, Dict, Optional

from requests import Session

from todoist_api_python.headers import create_headers


def get(
    session: Session,
    url: str,
    token: Optional[str] = None,
    params: Optional[Dict[str, Any]] = None,
):
    response = session.get(url, params=params, headers=create_headers(token=token))

    if response.status_code == 200:
        return response.json()

    response.raise_for_status()
    return response.ok


def post(
    session: Session,
    url: str,
    token: Optional[str] = None,
    data: Optional[Dict[str, Any]] = None,
):
    request_id = data.pop("request_id", None) if data else None

    headers = create_headers(
        token=token, with_content=True if data else False, request_id=request_id
    )

    response = session.post(
        url,
        headers=headers,
        data=json.dumps(data) if data else None,
    )

    if response.status_code == 200:
        return response.json()

    response.raise_for_status()
    return response.ok


def delete(
    session: Session,
    url: str,
    token: Optional[str] = None,
    args: Optional[Dict[str, Any]] = None,
):
    request_id = args.pop("request_id", None) if args else None

    headers = create_headers(token=token, request_id=request_id)

    response = session.delete(
        url,
        headers=headers,
    )

    response.raise_for_status()
    return response.ok
