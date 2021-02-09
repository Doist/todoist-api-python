from typing import Optional

SHOW_TASK_ENDPOINT = "https://todoist.com/showTask"


def get_url_for_task(task_id: int, sync_id: Optional[int]) -> str:
    return (
        f"{SHOW_TASK_ENDPOINT}?id={task_id}&sync_id={sync_id}"
        if sync_id
        else f"{SHOW_TASK_ENDPOINT}?id={task_id}"
    )
