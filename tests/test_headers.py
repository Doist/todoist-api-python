from todoist_api_python.headers import create_headers


def test_create_headers_none():
    headers = create_headers()
    assert headers == {}


def test_create_headers_authorization():
    token = "A Token"
    headers = create_headers(token=token)
    assert headers["Authorization"] == f"Bearer {token}"


def test_create_headers_request_id():
    request_id = "12345"
    headers = create_headers(request_id=request_id)
    assert headers["X-Request-Id"] == request_id


def test_create_headers_content_type():
    headers = create_headers(with_content=True)
    assert headers["Content-Type"] == "application/json; charset=utf-8"
