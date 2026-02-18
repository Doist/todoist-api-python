from __future__ import annotations

from tests.data.test_defaults import (
    DEFAULT_ATTACHMENT_RESPONSE,
    DEFAULT_COLLABORATOR_RESPONSE,
    DEFAULT_COMMENT_RESPONSE,
    DEFAULT_DUE_RESPONSE,
    DEFAULT_DURATION_RESPONSE,
    DEFAULT_FOLDER_RESPONSE,
    DEFAULT_LABEL_RESPONSE,
    DEFAULT_PROJECT_RESPONSE,
    DEFAULT_PROJECT_RESPONSE_2,
    DEFAULT_SECTION_RESPONSE,
    DEFAULT_TASK_RESPONSE,
)
from todoist_api_python._core.utils import parse_date, parse_datetime
from todoist_api_python.models import (
    Attachment,
    AuthResult,
    Collaborator,
    Comment,
    Due,
    Duration,
    Folder,
    Label,
    Project,
    Section,
    Task,
)

unexpected_data = {"unexpected_key": "some value"}


def test_due_from_dict() -> None:
    sample_data = dict(DEFAULT_DUE_RESPONSE)
    sample_data.update(unexpected_data)

    due = Due.from_dict(sample_data)

    assert due.date == parse_date(str(sample_data["date"]))
    assert due.timezone == sample_data["timezone"]
    assert due.string == sample_data["string"]
    assert due.lang == sample_data["lang"]
    assert due.is_recurring == sample_data["is_recurring"]


def test_duration_from_dict() -> None:
    sample_data = dict(DEFAULT_DURATION_RESPONSE)
    sample_data.update(unexpected_data)

    duration = Duration.from_dict(sample_data)

    assert duration.amount == sample_data["amount"]
    assert duration.unit == sample_data["unit"]


def test_project_from_dict() -> None:
    sample_data = dict(DEFAULT_PROJECT_RESPONSE)
    sample_data.update(unexpected_data)

    project = Project.from_dict(sample_data)

    assert project.id == sample_data["id"]
    assert project.name == sample_data["name"]
    assert project.description == sample_data["description"]
    assert project.parent_id == sample_data["parent_id"]
    assert project.folder_id == sample_data["folder_id"]
    assert project.workspace_id == sample_data["workspace_id"]
    assert project.order == sample_data["child_order"]
    assert project.color == sample_data["color"]
    assert project.is_collapsed == sample_data["collapsed"]
    assert project.is_shared == sample_data["shared"]
    assert project.is_favorite == sample_data["is_favorite"]
    assert project.is_inbox_project == sample_data["is_inbox_project"]
    assert project.can_assign_tasks == sample_data["can_assign_tasks"]
    assert project.view_style == sample_data["view_style"]
    assert project.created_at == parse_datetime(str(sample_data["created_at"]))
    assert project.updated_at == parse_datetime(str(sample_data["updated_at"]))


def test_project_url() -> None:
    inbox = Project.from_dict(dict(DEFAULT_PROJECT_RESPONSE))
    assert inbox.url == "https://app.todoist.com/app/inbox"
    project = Project.from_dict(dict(DEFAULT_PROJECT_RESPONSE_2))
    assert project.url == "https://app.todoist.com/app/project/inbox-6X7rfFVPjhvv84XG"


def test_task_from_dict() -> None:
    sample_data = dict(DEFAULT_TASK_RESPONSE)
    sample_data.update(unexpected_data)

    task = Task.from_dict(sample_data)

    assert task.id == sample_data["id"]
    assert task.content == sample_data["content"]
    assert task.description == sample_data["description"]
    assert task.project_id == sample_data["project_id"]
    assert task.section_id == sample_data["section_id"]
    assert task.parent_id == sample_data["parent_id"]
    assert task.labels == sample_data["labels"]
    assert task.priority == sample_data["priority"]
    assert task.due == Due.from_dict(sample_data["due"])
    assert task.duration == Duration.from_dict(sample_data["duration"])
    assert task.is_collapsed == sample_data["collapsed"]
    assert task.order == sample_data["child_order"]
    assert task.assignee_id == sample_data["responsible_uid"]
    assert task.assigner_id == sample_data["assigned_by_uid"]
    assert task.completed_at == sample_data["completed_at"]
    assert task.creator_id == sample_data["added_by_uid"]
    assert task.created_at == parse_datetime(sample_data["added_at"])
    assert task.updated_at == parse_datetime(sample_data["updated_at"])


def test_task_url() -> None:
    task = Task.from_dict(dict(DEFAULT_TASK_RESPONSE))
    assert (
        task.url
        == "https://app.todoist.com/app/task/some-task-content-6X7rM8997g3RQmvh"
    )


def test_section_from_dict() -> None:
    sample_data = dict(DEFAULT_SECTION_RESPONSE)
    sample_data.update(unexpected_data)

    section = Section.from_dict(sample_data)

    assert section.id == sample_data["id"]
    assert section.project_id == sample_data["project_id"]
    assert section.name == sample_data["name"]
    assert section.order == sample_data["order"]


def test_collaborator_from_dict() -> None:
    sample_data = dict(DEFAULT_COLLABORATOR_RESPONSE)
    sample_data.update(unexpected_data)

    collaborator = Collaborator.from_dict(sample_data)

    assert collaborator.id == sample_data["id"]
    assert collaborator.email == sample_data["email"]
    assert collaborator.name == sample_data["name"]


def test_attachment_from_dict() -> None:
    sample_data = dict(DEFAULT_ATTACHMENT_RESPONSE)
    sample_data.update(unexpected_data)

    attachment = Attachment.from_dict(sample_data)

    assert attachment.resource_type == sample_data["resource_type"]
    assert attachment.file_name == sample_data["file_name"]
    assert attachment.file_size == sample_data["file_size"]
    assert attachment.file_type == sample_data["file_type"]
    assert attachment.file_url == sample_data["file_url"]
    assert attachment.upload_state == sample_data["upload_state"]
    assert attachment.image == sample_data["image"]
    assert attachment.image_width == sample_data["image_width"]
    assert attachment.image_height == sample_data["image_height"]
    assert attachment.url == sample_data["url"]
    assert attachment.title == sample_data["title"]


def test_comment_from_dict() -> None:
    sample_data = dict(DEFAULT_COMMENT_RESPONSE)
    sample_data.update(unexpected_data)

    comment = Comment.from_dict(sample_data)

    assert comment.id == sample_data["id"]
    assert comment.content == sample_data["content"]
    assert comment.poster_id == sample_data["posted_uid"]
    assert comment.posted_at == parse_datetime(sample_data["posted_at"])
    assert comment.task_id == sample_data["task_id"]
    assert comment.project_id == sample_data["project_id"]
    assert comment.attachment == Attachment.from_dict(sample_data["attachment"])


def test_label_from_dict() -> None:
    sample_data = dict(DEFAULT_LABEL_RESPONSE)
    sample_data.update(unexpected_data)

    label = Label.from_dict(sample_data)

    assert label.id == sample_data["id"]
    assert label.name == sample_data["name"]
    assert label.color == sample_data["color"]
    assert label.order == sample_data["order"]
    assert label.is_favorite == sample_data["is_favorite"]


def test_folder_from_dict() -> None:
    sample_data = dict(DEFAULT_FOLDER_RESPONSE)
    sample_data.update(unexpected_data)

    folder = Folder.from_dict(sample_data)

    assert folder.id == sample_data["id"]
    assert folder.name == sample_data["name"]
    assert folder.workspace_id == sample_data["workspace_id"]
    assert folder.default_order == sample_data["default_order"]
    assert folder.child_order == sample_data["child_order"]
    assert folder.is_deleted == sample_data["is_deleted"]


def test_auth_result_from_dict() -> None:
    token = "123"
    state = "456"
    sample_data = {"access_token": token, "state": state}
    sample_data.update(unexpected_data)

    auth_result = AuthResult.from_dict(sample_data)

    assert auth_result.access_token == token
    assert auth_result.state == state
