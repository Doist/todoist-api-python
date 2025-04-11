from __future__ import annotations

import json
from typing import Any

import pytest
import responses
from requests import HTTPError, Session
from responses.matchers import query_param_matcher

from tests.data.test_defaults import DEFAULT_TOKEN
from tests.utils.test_utils import auth_matcher, param_matcher
from todoist_api_python._core.http_requests import delete, get, post

EXAMPLE_URL = "https://example.com/"
EXAMPLE_PARAMS = {"param1": "value1", "param2": "value2"}
EXAMPLE_DATA = {"param3": "value31", "param4": "value4"}
EXAMPLE_RESPONSE = {"result": "ok"}


@responses.activate
def test_get_with_params(default_task_response: dict[str, Any]) -> None:
    responses.add(
        method=responses.GET,
        url=EXAMPLE_URL,
        json=EXAMPLE_RESPONSE,
        status=200,
        match=[auth_matcher(), param_matcher(EXAMPLE_PARAMS)],
    )

    response: dict[str, Any] = get(
        session=Session(), url=EXAMPLE_URL, token=DEFAULT_TOKEN, params=EXAMPLE_PARAMS
    )

    assert len(responses.calls) == 1
    assert response == EXAMPLE_RESPONSE


@responses.activate
def test_get_raise_for_status() -> None:
    responses.add(
        method=responses.GET,
        url=EXAMPLE_URL,
        json="<error description>",
        status=500,
    )

    with pytest.raises(HTTPError) as error_info:
        get(Session(), EXAMPLE_URL, DEFAULT_TOKEN)

    assert error_info.value.response.content == b'"<error description>"'


@responses.activate
def test_post_with_data(default_task_response: dict[str, Any]) -> None:
    responses.add(
        method=responses.POST,
        url=EXAMPLE_URL,
        json=EXAMPLE_RESPONSE,
        status=200,
    )

    response: dict[str, Any] = post(
        session=Session(), url=EXAMPLE_URL, token=DEFAULT_TOKEN, data=EXAMPLE_DATA
    )

    assert len(responses.calls) == 1
    assert responses.calls[0].request.url == EXAMPLE_URL
    assert (
        responses.calls[0].request.headers["Authorization"] == f"Bearer {DEFAULT_TOKEN}"
    )
    assert (
        responses.calls[0].request.headers["Content-Type"]
        == "application/json; charset=utf-8"
    )
    assert responses.calls[0].request.body == json.dumps(EXAMPLE_DATA)
    assert response == EXAMPLE_RESPONSE


@responses.activate
def test_post_return_ok_when_no_response_body() -> None:
    responses.add(
        method=responses.POST,
        url=EXAMPLE_URL,
        status=204,
    )

    result: bool = post(session=Session(), url=EXAMPLE_URL, token=DEFAULT_TOKEN)
    assert result is True


@responses.activate
def test_post_raise_for_status() -> None:
    responses.add(
        method=responses.POST,
        url=EXAMPLE_URL,
        status=500,
    )

    with pytest.raises(HTTPError):
        post(session=Session(), url=EXAMPLE_URL, token=DEFAULT_TOKEN)


@responses.activate
def test_delete_with_params() -> None:
    responses.add(
        method=responses.DELETE,
        url=EXAMPLE_URL,
        status=204,
        match=[auth_matcher(), query_param_matcher(EXAMPLE_PARAMS)],
    )

    result = delete(
        session=Session(),
        url=EXAMPLE_URL,
        token=DEFAULT_TOKEN,
        params=EXAMPLE_PARAMS,
    )

    assert len(responses.calls) == 1
    assert result is True


@responses.activate
def test_delete_raise_for_status() -> None:
    responses.add(
        method=responses.DELETE,
        url=EXAMPLE_URL,
        status=500,
    )

    with pytest.raises(HTTPError):
        delete(session=Session(), url=EXAMPLE_URL, token=DEFAULT_TOKEN)
