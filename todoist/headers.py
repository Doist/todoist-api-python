import uuid
from typing import Dict, Optional

CONTENT_TYPE = ("Content-Type", "application/json; charset=utf-8")
AUTHORIZATION = ("Authorization", "Bearer %s")
X_REQUEST_ID = ("X-Request-Id", "%s")


def create_headers(
    token: Optional[str] = None,
    with_content: bool = False,
    with_request_id: bool = False,
) -> Dict[str, str]:
    headers: Dict[str, str] = {}

    if token:
        headers.update([(AUTHORIZATION[0], AUTHORIZATION[1] % token)])
    if with_content:
        headers.update([CONTENT_TYPE])
    if with_request_id:
        headers.update([(X_REQUEST_ID[0], X_REQUEST_ID[1] % str(uuid.uuid4()))])

    return headers
