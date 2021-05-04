# todoist-api-python
A python wrapper for the Todoist REST API.

### Installation

The repository can be included as a Poetry dependency in `pyproject.toml`, it is best to integrate to a release tag to ensure a stable dependency:

```
[tool.poetry.dependencies]
todoist-api-python = { git = "ssh://git@github.com/Doist/todoist-api-python.git", tag = "v1.x.x" }
```

### Usage

An example of initializing the API client and fetching a user's tasks:

```python
from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.api import TodoistAPI

# Fetch tasks asynchronously
async def get_tasks_async():
    api = TodoistAPIAsync("my token")
    try:
        tasks = await api.get_tasks()
        print(tasks)
    except Exception as error:
        print(error)

# Fetch tasks synchronously
def get_tasks_sync():
    api = TodoistAPI("my token")
    try:
        tasks = api.get_tasks()
        print(tasks)
    except Exception as error:
        print(error)
```

### Development

To install Python dependencies:

```sh
$ poetry install
```

To install pre-commit:

```sh
$ poetry run pre-commit install
```

### Releasing

The SDK is currently private so it not published to PyPI. To release a new update just create a release with a tag
in the format `v1.x.x` and any consumers can update to this tag in their `pyproject.toml`.
