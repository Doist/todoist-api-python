from tests.data.test_defaults import (
    DEFAULT_ATTACHMENT_RESPONSE,
    DEFAULT_COLLABORATOR_RESPONSE,
    DEFAULT_COMMENT_RESPONSE,
    DEFAULT_DUE_RESPONSE,
    DEFAULT_LABEL_RESPONSE,
    DEFAULT_PROJECT_RESPONSE,
    DEFAULT_SECTION_RESPONSE,
    DEFAULT_TASK_RESPONSE,
)
from todoist_api_python.models import (
    Attachment,
    Collaborator,
    Comment,
    Due,
    Label,
    Project,
    Section,
    Task,
)

unexpected_data = {"unexpected_key": "some value"}


def test_project_from_dict():
    sample_data = dict(DEFAULT_PROJECT_RESPONSE)
    sample_data.update(unexpected_data)

    project = Project.from_dict(sample_data)

    assert project.id == sample_data["id"]
    assert project.color == sample_data["color"]
    assert project.comment_count == sample_data["comment_count"]
    assert project.favorite == sample_data["favorite"]
    assert project.name == sample_data["name"]
    assert project.shared == sample_data["shared"]
    assert project.sync_id == sample_data["sync_id"]
    assert project.inbox_project == sample_data["inbox_project"]
    assert project.team_inbox == sample_data["team_inbox"]
    assert project.order == sample_data["order"]
    assert project.parent_id == sample_data["parent_id"]


def test_section_from_dict():
    sample_data = dict(DEFAULT_SECTION_RESPONSE)
    sample_data.update(unexpected_data)

    section = Section.from_dict(sample_data)

    assert section.id == sample_data["id"]
    assert section.name == sample_data["name"]
    assert section.order == sample_data["order"]
    assert section.project_id == sample_data["project_id"]


def test_due_from_dict():
    sample_data = dict(DEFAULT_DUE_RESPONSE)
    sample_data.update(unexpected_data)

    due = Due.from_dict(sample_data)

    assert due.date == sample_data["date"]
    assert due.recurring == sample_data["recurring"]
    assert due.string == sample_data["string"]
    assert due.datetime == sample_data["datetime"]
    assert due.timezone == sample_data["timezone"]


def test_task_from_dict():
    sample_data = dict(DEFAULT_TASK_RESPONSE)
    sample_data.update(unexpected_data)

    task = Task.from_dict(sample_data)

    assert task.comment_count == sample_data["comment_count"]
    assert task.completed == sample_data["completed"]
    assert task.content == sample_data["content"]
    assert task.created == sample_data["created"]
    assert task.creator == sample_data["creator"]
    assert task.id == sample_data["id"]
    assert task.project_id == sample_data["project_id"]
    assert task.section_id == sample_data["section_id"]
    assert task.priority == sample_data["priority"]
    assert task.url == sample_data["url"]
    assert task.assignee == sample_data["assignee"]
    assert task.assigner == sample_data["assigner"]
    assert task.due == Due.from_dict(sample_data["due"])
    assert task.label_ids == sample_data["label_ids"]
    assert task.order == sample_data["order"]
    assert task.parent_id == sample_data["parent_id"]
    assert task.sync_id == sample_data["sync_id"]


def test_collaborator_from_dict():
    sample_data = dict(DEFAULT_COLLABORATOR_RESPONSE)
    sample_data.update(unexpected_data)

    collaborator = Collaborator.from_dict(sample_data)

    assert collaborator.id == sample_data["id"]
    assert collaborator.email == sample_data["email"]
    assert collaborator.name == sample_data["name"]


def test_attachment_from_dict():
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


def test_comment_from_dict():
    sample_data = dict(DEFAULT_COMMENT_RESPONSE)
    sample_data.update(unexpected_data)

    comment = Comment.from_dict(sample_data)

    assert comment.id == sample_data["id"]
    assert comment.content == sample_data["content"]
    assert comment.posted == sample_data["posted"]
    assert comment.task_id == sample_data["task_id"]
    assert comment.project_id == sample_data["project_id"]
    assert comment.attachment == Attachment.from_dict(sample_data["attachment"])


def test_label_from_dict():
    sample_data = dict(DEFAULT_LABEL_RESPONSE)
    sample_data.update(unexpected_data)

    label = Label.from_dict(sample_data)

    assert label.id == sample_data["id"]
    assert label.name == sample_data["name"]
    assert label.color == sample_data["color"]
    assert label.order == sample_data["order"]
    assert label.favorite == sample_data["favorite"]
