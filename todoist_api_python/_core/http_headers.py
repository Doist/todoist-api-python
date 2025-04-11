from __future__ import annotations

CONTENT_TYPE = ("Content-Type", "application/json; charset=utf-8")
AUTHORIZATION = ("Authorization", "Bearer %s")


def create_headers(
    token: str | None = None,
    with_content: bool = False,
) -> dict[str, str]:
    headers: dict[str, str] = {}

    if token:
        headers.update([(AUTHORIZATION[0], AUTHORIZATION[1] % token)])
    if with_content:
        headers.update([CONTENT_TYPE])

    return headers
