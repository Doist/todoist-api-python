import json
import typing
from typing import Any, Dict, List

import pytest
import responses

from tests.data.test_defaults import (
    DEFAULT_REQUEST_ID,
    INVALID_ENTITY_ID,
    REST_API_BASE_URL,
)
from tests.utils.test_utils import (
    assert_auth_header,
    assert_id_validation,
    assert_request_id_header,
)
from todoist_api_python.api import TodoistAPI
from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.models import Comment


@pytest.mark.asyncio
async def test_get_comment(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_comment_response: Dict[str, Any],
    default_comment: Comment,
):
    comment_id = 1234
    expected_endpoint = f"{REST_API_BASE_URL}/comments/{comment_id}"

    requests_mock.add(
        responses.GET,
        expected_endpoint,
        json=default_comment_response,
        status=200,
    )

    comment = todoist_api.get_comment(comment_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert comment == default_comment

    comment = await todoist_api_async.get_comment(comment_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert comment == default_comment


@typing.no_type_check
def test_get_comment_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.get_comment(INVALID_ENTITY_ID), requests_mock
    )


@pytest.mark.asyncio
async def test_get_comments(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_comments_response: List[Dict[str, Any]],
    default_comments_list: List[Comment],
):
    task_id = 1234

    requests_mock.add(
        responses.GET,
        f"{REST_API_BASE_URL}/comments?task_id={task_id}",
        json=default_comments_response,
        status=200,
    )

    comments = todoist_api.get_comments(task_id=task_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert comments == default_comments_list

    comments = await todoist_api_async.get_comments(task_id=task_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert comments == default_comments_list


@pytest.mark.asyncio
async def test_add_comment(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
    default_comment_response: Dict[str, Any],
    default_comment: Comment,
):
    content = "A Comment"
    project_id = 123
    attachment_data = {
        "resource_type": "file",
        "file_url": "https://s3.amazonaws.com/domorebetter/Todoist+Setup+Guide.pdf",
        "file_type": "application/pdf",
        "file_name": "File.pdf",
    }

    expected_payload: Dict[str, Any] = {
        "content": content,
        "project_id": project_id,
        "attachment": attachment_data,
    }

    requests_mock.add(
        responses.POST,
        f"{REST_API_BASE_URL}/comments",
        json=default_comment_response,
        status=200,
    )

    new_comment = todoist_api.add_comment(
        content=content,
        project_id=project_id,
        attachment=attachment_data,
        request_id=DEFAULT_REQUEST_ID,
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(expected_payload)
    assert new_comment == default_comment

    new_comment = await todoist_api_async.add_comment(
        content=content,
        project_id=project_id,
        attachment=attachment_data,
        request_id=DEFAULT_REQUEST_ID,
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(expected_payload)
    assert new_comment == default_comment


@pytest.mark.asyncio
async def test_update_comment(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
):
    comment_id = 1234

    args = {
        "content": "An updated comment",
    }

    requests_mock.add(
        responses.POST, f"{REST_API_BASE_URL}/comments/{comment_id}", status=204
    )

    response = todoist_api.update_comment(
        comment_id=comment_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert_request_id_header(requests_mock.calls[0].request)
    assert requests_mock.calls[0].request.body == json.dumps(args)
    assert response is True

    response = await todoist_api_async.update_comment(
        comment_id=comment_id, request_id=DEFAULT_REQUEST_ID, **args
    )

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert_request_id_header(requests_mock.calls[1].request)
    assert requests_mock.calls[1].request.body == json.dumps(args)
    assert response is True


@typing.no_type_check
def test_update_comment_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.update_comment(INVALID_ENTITY_ID, "some new content"),
        requests_mock,
    )


@pytest.mark.asyncio
async def test_delete_comment(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: responses.RequestsMock,
):
    comment_id = 1234
    expected_endpoint = f"{REST_API_BASE_URL}/comments/{comment_id}"

    requests_mock.add(
        responses.DELETE,
        expected_endpoint,
        status=204,
    )

    response = todoist_api.delete_comment(comment_id)

    assert len(requests_mock.calls) == 1
    assert_auth_header(requests_mock.calls[0].request)
    assert response is True

    response = await todoist_api_async.delete_comment(comment_id)

    assert len(requests_mock.calls) == 2
    assert_auth_header(requests_mock.calls[1].request)
    assert response is True


@typing.no_type_check
def test_delete_comment_invalid_id(
    todoist_api: TodoistAPI,
    requests_mock: responses.RequestsMock,
):
    assert_id_validation(
        lambda: todoist_api.delete_comment(INVALID_ENTITY_ID),
        requests_mock,
    )
