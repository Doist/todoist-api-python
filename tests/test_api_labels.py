from __future__ import annotations

import json
from typing import TYPE_CHECKING, Any

import pytest
import responses

from tests.data.test_defaults import DEFAULT_REQUEST_ID, REST_API_BASE_URL
from tests.utils.test_utils import assert_auth_header, assert_request_id_header

if TYPE_CHECKING:
    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync
    from todoist_api_python.models import Label


@pytest.mark.asyncio
async def test_get_label(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_label_response: dict[str, Any],
    default_label: Label,
) -> None:
    label_id = "1234"
    expected_endpoint = f"{REST_API_BASE_URL}/labels/{label_id}"

    requests_mock.add(
        responses.GET,
        expected_endpoint,
        json=default_label_response,
        status=200,
    )

    label = todoist_api.get_label(label_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert label == default_label

    label = await todoist_api_async.get_label(label_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert label == default_label


@pytest.mark.asyncio
async def test_get_labels(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_labels_response: list[dict[str, Any]],
    default_labels_list: list[Label],
) -> None:
    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}/labels",
        json=default_labels_response,
        status=200,
    )

    labels = todoist_api.get_labels()

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert labels == default_labels_list

    labels = await todoist_api_async.get_labels()

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert labels == default_labels_list


@pytest.mark.asyncio
async def test_add_label_minimal(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_label_response: dict[str, Any],
    default_label: Label,
) -> None:
    label_name = "A Label"
    expected_payload = {"name": label_name}

    requests_mock.add(
        responses.POST,
        f"{REST_API_BASE_URL}/labels",
        json=default_label_response,
        status=200,
    )

    new_label = todoist_api.add_label(name=label_name, request_id=DEFAULT_REQUEST_ID)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(expected_payload)
    assert new_label == default_label

    new_label = await todoist_api_async.add_label(
        name=label_name, request_id=DEFAULT_REQUEST_ID
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(expected_payload)
    assert new_label == default_label


@pytest.mark.asyncio
async def test_add_label_full(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_label_response: dict[str, Any],
    default_label: Label,
) -> None:
    label_name = "A Label"

    optional_args = {
        "color": 30,
        "order": 3,
        "favorite": True,
    }

    expected_payload: dict[str, Any] = {"name": label_name}
    expected_payload.update(optional_args)

    requests_mock.add(
        responses.POST,
        f"{REST_API_BASE_URL}/labels",
        json=default_label_response,
        status=200,
    )

    new_label = todoist_api.add_label(
        name=label_name, request_id=DEFAULT_REQUEST_ID, **optional_args
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(expected_payload)
    assert new_label == default_label

    new_label = await todoist_api_async.add_label(
        name=label_name, request_id=DEFAULT_REQUEST_ID, **optional_args
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(expected_payload)
    assert new_label == default_label


@pytest.mark.asyncio
async def test_update_label(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
) -> None:
    label_id = "123"

    args = {
        "name": "An updated label",
        "order": 2,
        "color": 31,
        "favorite": False,
    }

    requests_mock.add(
        responses.POST, f"{REST_API_BASE_URL}/labels/{label_id}", status=204
    )

    response = todoist_api.update_label(
        label_id=label_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(args)
    assert response is True

    response = await todoist_api_async.update_label(
        label_id=label_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(args)
    assert response is True


@pytest.mark.asyncio
async def test_delete_label(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
) -> None:
    label_id = "1234"
    expected_endpoint = f"{REST_API_BASE_URL}/labels/{label_id}"

    requests_mock.add(
        responses.DELETE,
        expected_endpoint,
        status=204,
    )

    response = todoist_api.delete_label(label_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert response is True

    response = await todoist_api_async.delete_label(label_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert response is True
