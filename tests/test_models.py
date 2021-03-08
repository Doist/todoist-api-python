from tests.data.quick_add_responses import (
    QUICK_ADD_RESPONSE_FULL,
    QUICK_ADD_RESPONSE_MINIMAL,
)
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
    AuthResult,
    Collaborator,
    Comment,
    Due,
    Label,
    Project,
    QuickAddResult,
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
    assert project.url == sample_data["url"]
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


def test_quick_add_result_minimal():
    sample_data = dict(QUICK_ADD_RESPONSE_MINIMAL)
    sample_data.update(unexpected_data)

    quick_add_result = QuickAddResult.from_quick_add_response(sample_data)

    assert quick_add_result.task.comment_count == 0
    assert quick_add_result.task.completed is False
    assert quick_add_result.task.content == "some task"
    assert quick_add_result.task.created == "2021-02-05T11:02:56Z"
    assert quick_add_result.task.creator == 21180723
    assert quick_add_result.task.id == 4554989047
    assert quick_add_result.task.project_id == 2203108698
    assert quick_add_result.task.section_id == 0
    assert quick_add_result.task.priority == 1
    assert quick_add_result.task.url == "https://todoist.com/showTask?id=4554989047"
    assert quick_add_result.task.assignee is None
    assert quick_add_result.task.assigner is None
    assert quick_add_result.task.due is None
    assert quick_add_result.task.label_ids == []
    assert quick_add_result.task.order == 6
    assert quick_add_result.task.parent_id == 0
    assert quick_add_result.task.sync_id is None

    assert quick_add_result.resolved_assignee_name is None
    assert quick_add_result.resolved_label_names == []
    assert quick_add_result.resolved_project_name is None
    assert quick_add_result.resolved_section_name is None


def test_quick_add_result_full():
    sample_data = dict(QUICK_ADD_RESPONSE_FULL)
    sample_data.update(unexpected_data)

    quick_add_result = QuickAddResult.from_quick_add_response(sample_data)

    assert quick_add_result.task.comment_count == 0
    assert quick_add_result.task.completed is False
    assert quick_add_result.task.content == "some task"
    assert quick_add_result.task.created == "2021-02-05T11:04:54Z"
    assert quick_add_result.task.creator == 21180723
    assert quick_add_result.task.id == 4554993687
    assert quick_add_result.task.project_id == 2257514220
    assert quick_add_result.task.section_id == 2232454220
    assert quick_add_result.task.priority == 1
    assert (
        quick_add_result.task.url
        == "https://todoist.com/showTask?id=4554993687&sync_id=4554993687"
    )
    assert quick_add_result.task.assignee == 29172386
    assert quick_add_result.task.assigner == 21180723
    assert quick_add_result.task.due.date == "2021-02-06T11:00:00Z"
    assert quick_add_result.task.due.recurring is False
    assert quick_add_result.task.due.string == "Feb 6 11:00 AM"
    assert quick_add_result.task.due.datetime == "2021-02-06T11:00:00Z"
    assert quick_add_result.task.due.timezone == "Europe/London"
    assert quick_add_result.task.label_ids == [2156154810, 2156154812]
    assert quick_add_result.task.order == 1
    assert quick_add_result.task.parent_id == 0
    assert quick_add_result.task.sync_id == 4554993687

    assert quick_add_result.resolved_assignee_name == "Some Guy"
    assert quick_add_result.resolved_label_names == ["Label1", "Label2"]
    assert quick_add_result.resolved_project_name == "test"
    assert quick_add_result.resolved_section_name == "A section"


def test_quick_add_broken_data():
    none_attribute = QUICK_ADD_RESPONSE_FULL.copy()
    missing_attribute = QUICK_ADD_RESPONSE_FULL.copy()

    none_attribute["meta"]["project"] = None
    none_attribute["meta"]["assignee"] = None
    none_attribute["meta"]["section"] = None

    del missing_attribute["meta"]["project"]
    del missing_attribute["meta"]["assignee"]
    del missing_attribute["meta"]["section"]

    for quick_add_responses in [none_attribute, missing_attribute]:
        sample_data = dict(quick_add_responses)
        sample_data.update(unexpected_data)

        quick_add_result = QuickAddResult.from_quick_add_response(sample_data)

        assert quick_add_result.task.comment_count == 0
        assert quick_add_result.task.completed is False
        assert quick_add_result.task.content == "some task"
        assert quick_add_result.task.created == "2021-02-05T11:04:54Z"
        assert quick_add_result.task.creator == 21180723
        assert quick_add_result.task.id == 4554993687
        assert quick_add_result.task.project_id == 2257514220
        assert quick_add_result.task.section_id == 2232454220
        assert quick_add_result.task.priority == 1
        assert (
            quick_add_result.task.url
            == "https://todoist.com/showTask?id=4554993687&sync_id=4554993687"
        )
        assert quick_add_result.task.assignee == 29172386
        assert quick_add_result.task.assigner == 21180723
        assert quick_add_result.task.due.date == "2021-02-06T11:00:00Z"
        assert quick_add_result.task.due.recurring is False
        assert quick_add_result.task.due.string == "Feb 6 11:00 AM"
        assert quick_add_result.task.due.datetime == "2021-02-06T11:00:00Z"
        assert quick_add_result.task.due.timezone == "Europe/London"
        assert quick_add_result.task.label_ids == [2156154810, 2156154812]
        assert quick_add_result.task.order == 1
        assert quick_add_result.task.parent_id == 0
        assert quick_add_result.task.sync_id == 4554993687

        assert quick_add_result.resolved_assignee_name is None
        assert quick_add_result.resolved_label_names == ["Label1", "Label2"]
        assert quick_add_result.resolved_project_name is None
        assert quick_add_result.resolved_section_name is None


def test_auth_result_from_dict():
    token = "123"
    state = "456"
    sample_data = {"access_token": token, "state": state}
    sample_data.update(unexpected_data)

    auth_result = AuthResult.from_dict(sample_data)

    assert auth_result.access_token == token
    assert auth_result.state == state
