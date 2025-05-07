from __future__ import annotations

from todoist_api_python._core.http_headers import create_headers


def test_create_headers_default() -> None:
    headers = create_headers()
    assert headers == {}


def test_create_headers_authorization() -> None:
    token = "A Token"
    headers = create_headers(token=token)
    assert headers["Authorization"] == f"Bearer {token}"


def test_create_headers_content_type() -> None:
    headers = create_headers(with_content=True)
    assert headers["Content-Type"] == "application/json; charset=utf-8"


def test_create_headers_request_id() -> None:
    request_id = "12345"
    headers = create_headers(request_id=request_id)
    assert headers["X-Request-Id"] == request_id
