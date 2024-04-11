from tests.data.quick_add_responses import (
    QUICK_ADD_RESPONSE_FULL,
    QUICK_ADD_RESPONSE_MINIMAL,
)
from tests.data.test_defaults import (
    DEFAULT_ATTACHMENT_RESPONSE,
    DEFAULT_COLLABORATOR_RESPONSE,
    DEFAULT_COMMENT_RESPONSE,
    DEFAULT_COMPLETED_ITEMS_RESPONSE,
    DEFAULT_DUE_RESPONSE,
    DEFAULT_ITEM_COMPLETED_INFO_RESPONSE,
    DEFAULT_ITEM_RESPONSE,
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
    CompletedItems,
    Due,
    Item,
    ItemCompletedInfo,
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
    assert project.is_favorite == sample_data["is_favorite"]
    assert project.name == sample_data["name"]
    assert project.is_shared == sample_data["is_shared"]
    assert project.url == sample_data["url"]
    assert project.is_inbox_project == sample_data["is_inbox_project"]
    assert project.is_team_inbox == sample_data["is_team_inbox"]
    assert project.order == sample_data["order"]
    assert project.parent_id == sample_data["parent_id"]
    assert project.view_style == sample_data["view_style"]
    assert project.allow_assignment == sample_data["allow_assignment"]


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
    assert due.is_recurring == sample_data["is_recurring"]
    assert due.string == sample_data["string"]
    assert due.datetime == sample_data["datetime"]
    assert due.timezone == sample_data["timezone"]


def test_task_from_dict():
    sample_data = dict(DEFAULT_TASK_RESPONSE)
    sample_data.update(unexpected_data)

    task = Task.from_dict(sample_data)

    assert task.comment_count == sample_data["comment_count"]
    assert task.is_completed == sample_data["is_completed"]
    assert task.content == sample_data["content"]
    assert task.created_at == sample_data["created_at"]
    assert task.creator_id == sample_data["creator_id"]
    assert task.id == sample_data["id"]
    assert task.project_id == sample_data["project_id"]
    assert task.section_id == sample_data["section_id"]
    assert task.priority == sample_data["priority"]
    assert task.url == sample_data["url"]
    assert task.assignee_id == sample_data["assignee_id"]
    assert task.assigner_id == sample_data["assigner_id"]
    assert task.due == Due.from_dict(sample_data["due"])
    assert task.labels == sample_data["labels"]
    assert task.order == sample_data["order"]
    assert task.parent_id == sample_data["parent_id"]


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
    assert comment.posted_at == sample_data["posted_at"]
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
    assert label.is_favorite == sample_data["is_favorite"]


def test_quick_add_result_minimal():
    sample_data = dict(QUICK_ADD_RESPONSE_MINIMAL)
    sample_data.update(unexpected_data)

    quick_add_result = QuickAddResult.from_quick_add_response(sample_data)

    assert quick_add_result.task.comment_count == 0
    assert quick_add_result.task.is_completed is False
    assert quick_add_result.task.content == "some task"
    assert quick_add_result.task.created_at == "2021-02-05T11:02:56.00000Z"
    assert quick_add_result.task.creator_id == "21180723"
    assert quick_add_result.task.id == "4554989047"
    assert quick_add_result.task.project_id == "2203108698"
    assert quick_add_result.task.section_id is None
    assert quick_add_result.task.priority == 1
    assert quick_add_result.task.url == "https://todoist.com/showTask?id=4554989047"
    assert quick_add_result.task.assignee_id is None
    assert quick_add_result.task.assigner_id is None
    assert quick_add_result.task.due is None
    assert quick_add_result.task.labels == []
    assert quick_add_result.task.order == 6
    assert quick_add_result.task.parent_id is None
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
    assert quick_add_result.task.is_completed is False
    assert quick_add_result.task.content == "some task"
    assert quick_add_result.task.created_at == "2021-02-05T11:04:54.00000Z"
    assert quick_add_result.task.creator_id == "21180723"
    assert quick_add_result.task.id == "4554993687"
    assert quick_add_result.task.project_id == "2257514220"
    assert quick_add_result.task.section_id == "2232454220"
    assert quick_add_result.task.priority == 1
    assert (
        quick_add_result.task.url
        == "https://todoist.com/showTask?id=4554993687&sync_id=4554993687"
    )
    assert quick_add_result.task.assignee_id == "29172386"
    assert quick_add_result.task.assigner_id == "21180723"
    assert quick_add_result.task.due.date == "2021-02-06T11:00:00.00000Z"
    assert quick_add_result.task.due.is_recurring is False
    assert quick_add_result.task.due.string == "Feb 6 11:00 AM"
    assert quick_add_result.task.due.datetime == "2021-02-06T11:00:00.00000Z"
    assert quick_add_result.task.due.timezone == "Europe/London"
    assert quick_add_result.task.labels == ["Label1", "Label2"]
    assert quick_add_result.task.order == 1
    assert quick_add_result.task.parent_id is None
    assert quick_add_result.task.sync_id == "4554993687"

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
        assert quick_add_result.task.is_completed is False
        assert quick_add_result.task.content == "some task"
        assert quick_add_result.task.created_at == "2021-02-05T11:04:54.00000Z"
        assert quick_add_result.task.creator_id == "21180723"
        assert quick_add_result.task.id == "4554993687"
        assert quick_add_result.task.project_id == "2257514220"
        assert quick_add_result.task.section_id == "2232454220"
        assert quick_add_result.task.priority == 1
        assert (
            quick_add_result.task.url
            == "https://todoist.com/showTask?id=4554993687&sync_id=4554993687"
        )
        assert quick_add_result.task.assignee_id == "29172386"
        assert quick_add_result.task.assigner_id == "21180723"
        assert quick_add_result.task.due.date == "2021-02-06T11:00:00.00000Z"
        assert quick_add_result.task.due.is_recurring is False
        assert quick_add_result.task.due.string == "Feb 6 11:00 AM"
        assert quick_add_result.task.due.datetime == "2021-02-06T11:00:00.00000Z"
        assert quick_add_result.task.due.timezone == "Europe/London"
        assert quick_add_result.task.labels == ["Label1", "Label2"]
        assert quick_add_result.task.order == 1
        assert quick_add_result.task.parent_id is None
        assert quick_add_result.task.sync_id == "4554993687"

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


def test_item_from_dict():
    sample_data = dict(DEFAULT_ITEM_RESPONSE)
    sample_data.update(unexpected_data)

    item = Item.from_dict(sample_data)

    assert item.id == "2995104339"
    assert item.user_id == "2671355"
    assert item.project_id == "2203306141"
    assert item.content == "Buy Milk"
    assert item.description == ""
    assert item.priority == 1
    assert item.due.date == DEFAULT_DUE_RESPONSE["date"]
    assert item.due.is_recurring == DEFAULT_DUE_RESPONSE["is_recurring"]
    assert item.due.string == DEFAULT_DUE_RESPONSE["string"]
    assert item.due.datetime == DEFAULT_DUE_RESPONSE["datetime"]
    assert item.due.timezone == DEFAULT_DUE_RESPONSE["timezone"]
    assert item.parent_id is None
    assert item.child_order == 1
    assert item.section_id is None
    assert item.day_order == -1
    assert item.collapsed is False
    assert item.labels == ["Food", "Shopping"]
    assert item.added_by_uid == "2671355"
    assert item.assigned_by_uid == "2671355"
    assert item.responsible_uid is None
    assert item.checked is False
    assert item.is_deleted is False
    assert item.sync_id is None
    assert item.added_at == "2014-09-26T08:25:05.000000Z"


def test_item_completed_info_from_dict():
    sample_data = dict(DEFAULT_ITEM_COMPLETED_INFO_RESPONSE)
    sample_data.update(unexpected_data)

    info = ItemCompletedInfo.from_dict(sample_data)

    assert info.item_id == "2995104339"
    assert info.completed_items == 12


def test_completed_items_from_dict():
    sample_data = dict(DEFAULT_COMPLETED_ITEMS_RESPONSE)
    sample_data.update(unexpected_data)

    completed_items = CompletedItems.from_dict(sample_data)

    assert completed_items.total == 22
    assert completed_items.next_cursor == "k85gVI5ZAs8AAAABFoOzAQ"
    assert completed_items.has_more is True
    assert len(completed_items.items) == 1
    assert completed_items.items[0].id == "2995104339"
    assert completed_items.items[0].user_id == "2671355"
    assert completed_items.items[0].project_id == "2203306141"
    assert completed_items.items[0].content == "Buy Milk"
    assert completed_items.items[0].description == ""
    assert completed_items.items[0].priority == 1
    assert completed_items.items[0].due.date == DEFAULT_DUE_RESPONSE["date"]
    assert (
        completed_items.items[0].due.is_recurring
        == DEFAULT_DUE_RESPONSE["is_recurring"]
    )
    assert completed_items.items[0].due.string == DEFAULT_DUE_RESPONSE["string"]
    assert completed_items.items[0].due.datetime == DEFAULT_DUE_RESPONSE["datetime"]
    assert completed_items.items[0].due.timezone == DEFAULT_DUE_RESPONSE["timezone"]
    assert completed_items.items[0].parent_id is None
    assert completed_items.items[0].child_order == 1
    assert completed_items.items[0].section_id is None
    assert completed_items.items[0].day_order == -1
    assert completed_items.items[0].collapsed is False
    assert completed_items.items[0].labels == ["Food", "Shopping"]
    assert completed_items.items[0].added_by_uid == "2671355"
    assert completed_items.items[0].assigned_by_uid == "2671355"
    assert completed_items.items[0].responsible_uid is None
    assert completed_items.items[0].checked is False
    assert completed_items.items[0].is_deleted is False
    assert completed_items.items[0].sync_id is None
    assert completed_items.items[0].added_at == "2014-09-26T08:25:05.000000Z"
    assert len(completed_items.completed_info) == 1
    assert completed_items.completed_info[0].item_id == "2995104339"
    assert completed_items.completed_info[0].completed_items == 12
