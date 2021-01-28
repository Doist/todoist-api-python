import json

import pytest
import responses
from requests import HTTPError, Session

from tests.conftest import DEFAULT_TOKEN
from tests.data.test_defaults import DEFAULT_TASK_DATA
from todoist_api_python.http_requests import delete, get, post

DEFAULT_URL = "https://api.todoist.com/someurl"


@responses.activate
def test_get_with_params():
    params = {"param1": "value1", "param2": "value2"}

    responses.add(
        responses.GET,
        DEFAULT_URL,
        json=DEFAULT_TASK_DATA,
        status=200,
    )

    response = get(Session(), DEFAULT_TOKEN, DEFAULT_URL, params)

    assert len(responses.calls) == 1
    assert (
        responses.calls[0].request.url == f"{DEFAULT_URL}?param1=value1&param2=value2"
    )
    assert (
        responses.calls[0].request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"
    )
    assert response == DEFAULT_TASK_DATA


@responses.activate
def test_get_raise_for_status():
    with pytest.raises(HTTPError):
        responses.add(
            responses.GET,
            DEFAULT_URL,
            status=500,
        )

        get(Session(), DEFAULT_TOKEN, DEFAULT_URL)


@responses.activate
def test_post_with_data():
    request_id = "12345"

    data = {"param1": "value1", "param2": "value2", "request_id": request_id}

    responses.add(
        responses.POST,
        DEFAULT_URL,
        json=DEFAULT_TASK_DATA,
        status=200,
    )

    response = post(Session(), DEFAULT_TOKEN, DEFAULT_URL, data)

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == DEFAULT_URL
    assert (
        responses.calls[0].request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"
    )
    assert responses.calls[0].request.headers["X-Request-Id"] == request_id
    assert (
        responses.calls[0].request.headers["Content-Type"]
        == "application/json; charset=utf-8"
    )
    assert responses.calls[0].request.body == json.dumps(data)
    assert response == DEFAULT_TASK_DATA


@responses.activate
def test_post_return_ok_when_no_response_body():
    responses.add(
        responses.POST,
        DEFAULT_URL,
        status=204,
    )

    result = post(Session(), DEFAULT_TOKEN, DEFAULT_URL)

    assert result is True


@responses.activate
def test_post_raise_for_status():
    with pytest.raises(HTTPError):
        responses.add(
            responses.POST,
            DEFAULT_URL,
            status=500,
        )

        post(Session(), DEFAULT_TOKEN, DEFAULT_URL)


@responses.activate
def test_delete_with_request_id():
    request_id = "12345"

    responses.add(
        responses.DELETE,
        DEFAULT_URL,
        status=204,
    )

    result = delete(Session(), DEFAULT_TOKEN, DEFAULT_URL, {"request_id": request_id})

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == DEFAULT_URL
    assert (
        responses.calls[0].request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"
    )
    assert responses.calls[0].request.headers["X-Request-Id"] == request_id
    assert result is True


@responses.activate
def test_delete_raise_for_status():
    with pytest.raises(HTTPError):
        responses.add(
            responses.DELETE,
            DEFAULT_URL,
            status=500,
        )

        delete(Session(), DEFAULT_TOKEN, DEFAULT_URL)
