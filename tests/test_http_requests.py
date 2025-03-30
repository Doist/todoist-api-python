from __future__ import annotations

import json
from typing import Any

import pytest
import responses
from requests import HTTPError, Session

from tests.conftest import DEFAULT_TOKEN
from todoist_api_python.endpoints import BASE_URL, TASKS_ENDPOINT
from todoist_api_python.http_requests import delete, get, post

DEFAULT_URL = f"{BASE_URL}/{TASKS_ENDPOINT}"


@responses.activate
def test_get_with_params(default_task_response: dict[str, Any]) -> None:
    params = {"param1": "value1", "param2": "value2"}

    responses.add(
        responses.GET,
        DEFAULT_URL,
        json=default_task_response,
        status=200,
    )

    response = get(Session(), DEFAULT_URL, DEFAULT_TOKEN, params)

    assert len(responses.calls) == 1
    assert (
        responses.calls[0].request.url == f"{DEFAULT_URL}?param1=value1&param2=value2"
    )
    assert (
        responses.calls[0].request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"
    )
    assert response == default_task_response


@responses.activate
def test_get_raise_for_status() -> None:
    responses.add(
        responses.GET,
        DEFAULT_URL,
        status=500,
    )

    with pytest.raises(HTTPError):
        get(Session(), DEFAULT_URL, DEFAULT_TOKEN)


@responses.activate
def test_post_with_data(default_task_response: dict[str, Any]) -> None:
    request_id = "12345"

    data = {"param1": "value1", "param2": "value2", "request_id": request_id}

    responses.add(
        responses.POST,
        DEFAULT_URL,
        json=default_task_response,
        status=200,
    )

    response = post(Session(), DEFAULT_URL, DEFAULT_TOKEN, data)

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
    assert response == default_task_response


@responses.activate
def test_post_return_ok_when_no_response_body() -> None:
    responses.add(
        responses.POST,
        DEFAULT_URL,
        status=204,
    )

    result = post(Session(), DEFAULT_URL, DEFAULT_TOKEN)

    assert result is True


@responses.activate
def test_post_raise_for_status() -> None:
    responses.add(
        responses.POST,
        DEFAULT_URL,
        status=500,
    )

    with pytest.raises(HTTPError):
        post(Session(), DEFAULT_URL, DEFAULT_TOKEN)


@responses.activate
def test_delete_with_request_id() -> None:
    request_id = "12345"

    responses.add(
        responses.DELETE,
        DEFAULT_URL,
        status=204,
    )

    result = delete(Session(), DEFAULT_URL, DEFAULT_TOKEN, {"request_id": request_id})

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == DEFAULT_URL
    assert (
        responses.calls[0].request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"
    )
    assert responses.calls[0].request.headers["X-Request-Id"] == request_id
    assert result is True


@responses.activate
def test_delete_raise_for_status() -> None:
    responses.add(
        responses.DELETE,
        DEFAULT_URL,
        status=500,
    )

    with pytest.raises(HTTPError):
        delete(Session(), DEFAULT_URL, DEFAULT_TOKEN)
