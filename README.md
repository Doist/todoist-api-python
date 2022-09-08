# Todoist API Python Client

This is the official Python API client for the Todoist REST API.

### Installation

The repository can be included as a Poetry dependency in `pyproject.toml`, it is best to integrate to a release tag to ensure a stable dependency:

```
[tool.poetry.dependencies]
todoist-api-python = "^v2.0.0"
```

### Supported Python Versions

Python 3.9 is fully supported and tested, and while it may work with other Python 3 versions, we do not test for them.

### Usage

An example of initializing the API client and fetching a user's tasks:

```python
from todoist_api_python.api_async import TodoistAPIAsync
from todoist_api_python.api import TodoistAPI

# Fetch tasks asynchronously
async def get_tasks_async():
    api = TodoistAPIAsync("YOURTOKEN")
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

### Documentation

For more detailed reference documentation, have a look at the [API documentation with Python examples](https://developer.todoist.com/rest/v2/?python).

### Development

To install Python dependencies:

```sh
$ poetry install
```

To install pre-commit:

```sh
$ poetry run pre-commit install
```

You can try your changes via REPL by running:

```sh
$ poetry run python
```

You can then import the library as describe in [Usage](#usage) without having to create a file. Keep in mind that you have to `import asyncio` and run `asyncio.run(yourmethod())` to make your async methods run as expected if you decide to use `TodoistAPIAsync`.

### Releases

This API client is public, and available in a PyPI repository.

A new update is automatically released by GitHub Actions, by creating a release with a tag in the format `vX.Y.Z` (`v<Major>.<Minor>.<Patch>`).

Users of the API client can then update to the new version in their `pyproject.toml` file.

### Feedback

Any feedback, such as bugs, questions, comments, etc. can be reported as *Issues* in this repository, and will be handled by Doist.

### Contributions

We would love contributions in the form of *Pull requests* in this repository.
