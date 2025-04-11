# Todoist API Python Client

This is the official Python SDK for the Todoist API.

## Installation

```bash
pip install todoist-api-python
```

Or add the project as a dependency in `pyproject.toml`:

```toml
dependencies = [
  "todoist-api-python>=3.0.0,<4",
]
```

### Supported Python Versions

While we only actively test under Python 3.13, we strive to support all versions from Python 3.9 and above.

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

## Documentation

For more detailed reference documentation, have a look at the [SDK documentation](https://doist.github.io/todoist-api-python/) and the [API documentation](https://developer.todoist.com).

## Development

To install Python dependencies:

```sh
$ uv sync
```

To install pre-commit:

```sh
$ uv run pre-commit install
```

You can try your changes via REPL by running:

```sh
$ uv run python
```

You can then import the library as described in [Usage](#usage) without having to create a file.
If you decide to use `TodoistAPIAsync`, please keep in mind that you have to `import asyncio`
and run `asyncio.run(yourmethod())` to make your async methods run as expected.

### Releases

This API client is public, and available in a PyPI repository.

A new update is automatically released by GitHub Actions, by creating a release with a tag in the format `vX.Y.Z` (`v<Major>.<Minor>.<Patch>`).

Users of the API client can then update to the new version in their `pyproject.toml` file.

## Feedback

Any feedback, bugs, questions, comments, etc., can be reported as *Issues* in this repository.

### Contributions

We would love contributions! *Pull requests* are welcome.
