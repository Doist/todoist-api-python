from __future__ import annotations

from typing import TYPE_CHECKING, Any

import httpx
import pytest

from tests.data.test_defaults import DEFAULT_REQUEST_ID, DEFAULT_TOKEN
from tests.utils.test_utils import api_headers, mock_route
from todoist_api_python._core.http_requests import delete, get, post

if TYPE_CHECKING:
    import respx

EXAMPLE_URL = "https://example.com/"
EXAMPLE_PARAMS = {"param1": "value1", "param2": "value2"}
EXAMPLE_DATA = {"param3": "value31", "param4": "value4"}
EXAMPLE_RESPONSE = {"result": "ok"}


def test_get_with_params(respx_mock: respx.MockRouter) -> None:
    mock_route(
        respx_mock,
        method="GET",
        url=EXAMPLE_URL,
        request_params=EXAMPLE_PARAMS,
        request_headers=api_headers(request_id=DEFAULT_REQUEST_ID),
        response_json=EXAMPLE_RESPONSE,
        response_status=200,
    )

    with httpx.Client() as client:
        response: dict[str, Any] = get(
            client=client,
            url=EXAMPLE_URL,
            token=DEFAULT_TOKEN,
            request_id=DEFAULT_REQUEST_ID,
            params=EXAMPLE_PARAMS,
        )

    assert len(respx_mock.calls) == 1
    assert response == EXAMPLE_RESPONSE


def test_get_raise_for_status(respx_mock: respx.MockRouter) -> None:
    mock_route(
        respx_mock,
        method="GET",
        url=EXAMPLE_URL,
        response_json="<error description>",
        response_status=500,
    )

    with httpx.Client() as client, pytest.raises(httpx.HTTPStatusError) as error_info:
        get(client, EXAMPLE_URL, DEFAULT_TOKEN)

    assert error_info.value.response.content == b'"<error description>"'


def test_post_with_data(respx_mock: respx.MockRouter) -> None:
    mock_route(
        respx_mock,
        method="POST",
        url=EXAMPLE_URL,
        request_headers=api_headers(request_id=DEFAULT_REQUEST_ID),
        request_json=EXAMPLE_DATA,
        response_json=EXAMPLE_RESPONSE,
        response_status=200,
    )

    with httpx.Client() as client:
        response: dict[str, Any] = post(
            client=client,
            url=EXAMPLE_URL,
            token=DEFAULT_TOKEN,
            request_id=DEFAULT_REQUEST_ID,
            data=EXAMPLE_DATA,
        )

    assert len(respx_mock.calls) == 1
    assert response == EXAMPLE_RESPONSE


def test_post_with_empty_data(respx_mock: respx.MockRouter) -> None:
    mock_route(
        respx_mock,
        method="POST",
        url=EXAMPLE_URL,
        request_headers=api_headers(request_id=DEFAULT_REQUEST_ID),
        request_json={},
        response_json=EXAMPLE_RESPONSE,
        response_status=200,
    )

    with httpx.Client() as client:
        response: dict[str, Any] = post(
            client=client,
            url=EXAMPLE_URL,
            token=DEFAULT_TOKEN,
            request_id=DEFAULT_REQUEST_ID,
            data={},
        )

    assert len(respx_mock.calls) == 1
    assert response == EXAMPLE_RESPONSE


def test_post_return_ok_when_no_response_body(respx_mock: respx.MockRouter) -> None:
    mock_route(
        respx_mock,
        method="POST",
        url=EXAMPLE_URL,
        response_status=204,
    )

    with httpx.Client() as client:
        result: bool = post(client=client, url=EXAMPLE_URL, token=DEFAULT_TOKEN)

    assert result is True


def test_post_raise_for_status(respx_mock: respx.MockRouter) -> None:
    mock_route(
        respx_mock,
        method="POST",
        url=EXAMPLE_URL,
        response_status=500,
    )

    with httpx.Client() as client, pytest.raises(httpx.HTTPStatusError):
        post(client=client, url=EXAMPLE_URL, token=DEFAULT_TOKEN)


def test_delete_with_params(respx_mock: respx.MockRouter) -> None:
    mock_route(
        respx_mock,
        method="DELETE",
        url=EXAMPLE_URL,
        request_params=EXAMPLE_PARAMS,
        request_headers=api_headers(request_id=DEFAULT_REQUEST_ID),
        response_status=204,
    )

    with httpx.Client() as client:
        result = delete(
            client=client,
            url=EXAMPLE_URL,
            token=DEFAULT_TOKEN,
            request_id=DEFAULT_REQUEST_ID,
            params=EXAMPLE_PARAMS,
        )

    assert len(respx_mock.calls) == 1
    assert result is True


def test_delete_raise_for_status(respx_mock: respx.MockRouter) -> None:
    mock_route(
        respx_mock,
        method="DELETE",
        url=EXAMPLE_URL,
        response_status=500,
    )

    with httpx.Client() as client, pytest.raises(httpx.HTTPStatusError):
        delete(client=client, url=EXAMPLE_URL, token=DEFAULT_TOKEN)
