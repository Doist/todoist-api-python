from todoist.api import TodoistAPI


def run():
    api = TodoistAPI("e636d34f7bb627476bf99397f00be2bb3c7d0b6e")
    result = api.delete_task(task_id=4525827898)
    print(result)


run()
