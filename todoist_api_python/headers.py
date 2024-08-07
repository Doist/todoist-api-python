from __future__ import annotations

CONTENT_TYPE = ("Content-Type", "application/json; charset=utf-8")
AUTHORIZATION = ("Authorization", "Bearer %s")
X_REQUEST_ID = ("X-Request-Id", "%s")


def create_headers(
    token: str | None = None,
    with_content: bool = False,
    request_id: str | None = None,
) -> dict[str, str]:
    headers: dict[str, str] = {}

    if token:
        headers.update([(AUTHORIZATION[0], AUTHORIZATION[1] % token)])
    if with_content:
        headers.update([CONTENT_TYPE])
    if request_id:
        headers.update([(X_REQUEST_ID[0], X_REQUEST_ID[1] % request_id)])

    return headers
