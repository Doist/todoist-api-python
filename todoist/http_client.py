import json
from typing import Any, Dict, Optional

import requests

from todoist.headers import create_headers


def get(token: str, url: str, params: Optional[Dict[str, Any]] = None):
    response = requests.get(url, params=params, headers=create_headers(token=token))

    if response.status_code == 200:
        return response.json()

    response.raise_for_status()
    return response.ok


def post(token: str, url: str, data: Optional[Dict] = None):
    headers = create_headers(
        token=token, with_content=True if data else False, with_request_id=True
    )

    response = requests.post(
        url,
        headers=headers,
        data=json.dumps(data) if data else None,
    )

    if response.status_code == 200:
        return response.json()

    response.raise_for_status()
    return response.ok


def delete(token: str, url: str):
    headers = create_headers(token=token, with_request_id=True)

    response = requests.delete(
        url,
        headers=headers,
    )

    response.raise_for_status()
    return response.ok
