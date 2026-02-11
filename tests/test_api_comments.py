from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest

from tests.data.test_defaults import (
    DEFAULT_API_URL,
    PaginatedResults,
)
from tests.utils.test_utils import (
    auth_matcher,
    data_matcher,
    enumerate_async,
    param_matcher,
    request_id_matcher,
)
from todoist_api_python.models import Attachment

if TYPE_CHECKING:
    from tests.utils.http_mock import RequestsMock
    from todoist_api_python.api import TodoistAPI
    from todoist_api_python.api_async import TodoistAPIAsync

from todoist_api_python.models import Comment


@pytest.mark.asyncio
async def test_get_comment(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_comment_response: dict[str, Any],
    default_comment: Comment,
) -> None:
    comment_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/comments/{comment_id}"

    requests_mock.add(
        method="GET",
        url=endpoint,
        json=default_comment_response,
        status=200,
        match=[auth_matcher(), request_id_matcher()],
    )

    comment = todoist_api.get_comment(comment_id)

    assert len(requests_mock.calls) == 1
    assert comment == default_comment

    comment = await todoist_api_async.get_comment(comment_id)

    assert len(requests_mock.calls) == 2
    assert comment == default_comment


@pytest.mark.asyncio
async def test_get_comments(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_comments_response: list[PaginatedResults],
    default_comments_list: list[list[Comment]],
) -> None:
    task_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/comments"

    cursor: str | None = None
    for page in default_comments_response:
        requests_mock.add(
            method="GET",
            url=endpoint,
            json=page,
            status=200,
            match=[
                auth_matcher(),
                request_id_matcher(),
                param_matcher({"task_id": task_id}, cursor),
            ],
        )
        cursor = page["next_cursor"]

    count = 0

    comments_iter = todoist_api.get_comments(task_id=task_id)

    for i, comments in enumerate(comments_iter):
        assert len(requests_mock.calls) == count + 1
        assert comments == default_comments_list[i]
        count += 1

    comments_async_iter = await todoist_api_async.get_comments(task_id=task_id)

    async for i, comments in enumerate_async(comments_async_iter):
        assert len(requests_mock.calls) == count + 1
        assert comments == default_comments_list[i]
        count += 1


@pytest.mark.asyncio
async def test_add_comment(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_comment_response: dict[str, Any],
    default_comment: Comment,
) -> None:
    content = "A Comment"
    project_id = "6HWcc9PJCvPjCxC9"
    attachment = Attachment(
        resource_type="file",
        file_url="https://s3.amazonaws.com/domorebetter/Todoist+Setup+Guide.pdf",
        file_type="application/pdf",
        file_name="File.pdf",
    )

    requests_mock.add(
        method="POST",
        url=f"{DEFAULT_API_URL}/comments",
        json=default_comment_response,
        status=200,
        match=[
            auth_matcher(),
            request_id_matcher(),
            data_matcher(
                {
                    "content": content,
                    "project_id": project_id,
                    "attachment": attachment.to_dict(),
                }
            ),
        ],
    )

    new_comment = todoist_api.add_comment(
        content=content,
        project_id=project_id,
        attachment=attachment,
    )

    assert len(requests_mock.calls) == 1
    assert new_comment == default_comment

    new_comment = await todoist_api_async.add_comment(
        content=content,
        project_id=project_id,
        attachment=attachment,
    )

    assert len(requests_mock.calls) == 2
    assert new_comment == default_comment


@pytest.mark.asyncio
async def test_update_comment(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
    default_comment: Comment,
) -> None:
    args = {
        "content": "An updated comment",
    }
    updated_comment_dict = default_comment.to_dict() | args

    requests_mock.add(
        method="POST",
        url=f"{DEFAULT_API_URL}/comments/{default_comment.id}",
        json=updated_comment_dict,
        status=200,
        match=[auth_matcher(), request_id_matcher(), data_matcher(args)],
    )

    response = todoist_api.update_comment(comment_id=default_comment.id, **args)

    assert len(requests_mock.calls) == 1
    assert response == Comment.from_dict(updated_comment_dict)

    response = await todoist_api_async.update_comment(
        comment_id=default_comment.id, **args
    )

    assert len(requests_mock.calls) == 2
    assert response == Comment.from_dict(updated_comment_dict)


@pytest.mark.asyncio
async def test_delete_comment(
    todoist_api: TodoistAPI,
    todoist_api_async: TodoistAPIAsync,
    requests_mock: RequestsMock,
) -> None:
    comment_id = "6X7rM8997g3RQmvh"
    endpoint = f"{DEFAULT_API_URL}/comments/{comment_id}"

    requests_mock.add(
        method="DELETE",
        url=endpoint,
        status=204,
        match=[auth_matcher(), request_id_matcher()],
    )

    response = todoist_api.delete_comment(comment_id)

    assert len(requests_mock.calls) == 1
    assert response is True

    response = await todoist_api_async.delete_comment(comment_id)

    assert len(requests_mock.calls) == 2
    assert response is True
