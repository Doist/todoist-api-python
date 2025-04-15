# Overview

This is the official Python SDK for the Todoist API.

## Installation

```bash
pip install todoist-api-python
```

Or add the project as a dependency in `pyproject.toml`:

```toml
dependencies = [
  "todoist-api-python>=3.0.1,<4",
]
```

## Usage

Here's an example of initializing the API client, fetching a task, and paginating through its comments:

```python
from todoist_api_python.api import TodoistAPI

api = TodoistAPI("YOUR_API_TOKEN")

task = api.get_task("6X4Vw2Hfmg73Q2XR")
print(f"Task: {task.content}")

comments_iter = api.get_comments(task_id=task.id)
for comments in comments_iter:
    for comment in comments:
        print(f"Comment: {comment.content}")
```

## Quick start

- [Authentication](authentication.md)
- [API client](api.md)
- [Models](models.md)

## API reference

For detailed reference documentation, have a look at the [API documentation](https://developer.todoist.com/).
