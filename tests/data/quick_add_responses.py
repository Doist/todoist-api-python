from __future__ import annotations

from typing import Any

from tests.data.test_defaults import DEFAULT_DURATION_RESPONSE

QUICK_ADD_RESPONSE_MINIMAL: dict[str, Any] = {
    "added_by_uid": "21180723",
    "assigned_by_uid": None,
    "checked": 0,
    "child_order": 6,
    "collapsed": 0,
    "content": "some task",
    "description": "",
    "added_at": "2021-02-05T11:02:56.00000Z",
    "date_completed": None,
    "due": None,
    "duration": None,
    "id": "4554989047",
    "in_history": 0,
    "is_deleted": 0,
    "labels": [],
    "meta": {
        "assignee": [None, None],
        "due": {
            "date_local": None,
            "datetime_local": None,
            "datetime_utc": None,
            "is_recurring": False,
            "lang": None,
            "object_type": "null",
            "string": None,
            "timezone": None,
            "timezone_name": None,
        },
        "labels": {},
        "priority": 1,
        "project": [None, None],
        "section": [None, None],
        "text": "some task",
    },
    "parent_id": None,
    "priority": 1,
    "project_id": "2203108698",
    "responsible_uid": None,
    "section_id": None,
    "sync_id": None,
    "user_id": "21180723",
}

QUICK_ADD_RESPONSE_FULL: dict[str, Any] = {
    "added_by_uid": "21180723",
    "assigned_by_uid": "21180723",
    "checked": 0,
    "child_order": 1,
    "collapsed": 0,
    "content": "some task",
    "description": "a description",
    "added_at": "2021-02-05T11:04:54.00000Z",
    "date_completed": None,
    "due": {
        "date": "2021-02-06T11:00:00.00000Z",
        "is_recurring": False,
        "lang": "en",
        "string": "Feb 6 11:00 AM",
        "timezone": "Europe/London",
    },
    "duration": {
        "amount": 60,
        "unit": "minute",
    },
    "id": "4554993687",
    "in_history": 0,
    "is_deleted": 0,
    "labels": ["Label1", "Label2"],
    "meta": {
        "assignee": ["29172386", "Some Guy"],
        "due": {
            "date_local": "2021-02-06T00:00:00.00000Z",
            "datetime_local": "2021-02-06T11:00:00.00000Z",
            "datetime_utc": "2021-02-06T11:00:00.00000Z",
            "is_recurring": False,
            "lang": "en",
            "object_type": "fixed_datetime",
            "string": "Feb 6 11:00 AM",
            "timezone": {"zone": "Europe/London"},
            "timezone_name": "Europe/London",
        },
        "labels": {"2156154810": "Label1", "2156154812": "Label2"},
        "priority": 1,
        "project": ["2257514220", "test"],
        "section": ["2232454220", "A section"],
        "text": "some task",
    },
    "parent_id": None,
    "priority": 1,
    "project_id": "2257514220",
    "responsible_uid": "29172386",
    "section_id": "2232454220",
    "sync_id": "4554993687",
    "user_id": "21180723",
}
