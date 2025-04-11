from __future__ import annotations

from todoist_api_python._core.http_headers import create_headers


def test_create_headers_none() -> None:
    headers = create_headers()
    assert headers == {}


def test_create_headers_authorization() -> None:
    token = "A Token"
    headers = create_headers(token=token)
    assert headers["Authorization"] == f"Bearer {token}"


def test_create_headers_content_type() -> None:
    headers = create_headers(with_content=True)
    assert headers["Content-Type"] == "application/json; charset=utf-8"
