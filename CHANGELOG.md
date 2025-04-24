# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- Compatibility with Python 3.9 and Python 3.10

## [3.0.1] - 2025-04-15

### Fixed

- Wheel and source distributions didn't include the package itself
- Project requiring Python 3.13 to be installed

## [3.0.0] - 2025-04-11

### Added

- Support for deadlines
- Support for archiving and unarchiving projects
- Support for fetching completed tasks by due date range and by completion date range
- Support for `note`, `reminder`, and `auto_reminder` in `add_task_quick`
- Documentation for all SDK functions, arguments, and return objects
- Types, type hints for all SDK functions, arguments, and return objects
- Function to obtain project URLs

### Changed

- Use `dataclass-wizard` for object mapping
- Modernized SDK to use the Todoist API v1
  - Remove deprecated `Task.sync_id`, `Task.comment_count`, and `Project.comment_count`
  - Replace `Task.is_completed` with `Task.completed_at`
  - Add support for `calendar` in `Project.view_style`
  - Rename `quick_add_task` to `add_task_quick`
  - Add `filter_tasks`, extracting that workflow from `get_tasks`
  - Paginate results via an `Iterator` in `get_tasks`, `filter_task`, `get_projects`,
  `get_collaborators`, `get_sections`, `get_comments`, `get_labels`, `get_shared_labels`
  - Receive `date` and `datetime` arguments as objects, not strings
  - Remove support for `X-Request-Id` header, unused on the API level
- "Hide" internal modules and functions
- Task URLs are now obtained on demand, improving performance when not needed

### Fixed

- API requests configure appropriate timeouts to avoid connections hanging

## [2.1.7] - 2024-08-13

### Fixes

- Regression with some `Project` object attributes

## [2.1.6] - 2024-08-07

### Fixes

- `TodoistAPIAsync` accepts a `session` parameter
- State becomes optional in `AuthResult.from_dict()`
- Duration handling in `to_dict()` and tests
- Default value to `section_id`
- Properly close requests `Session` object

## [2.1.5] - 2024-05-22

### Fixes

- Key error on `can_assign_tasks` in `Project` model

## [2.1.4] - 2024-05-07

### Added

- Support `project.can_assign_tasks`
- Add `duration` to `Task` object
- Pagination example

## [2.1.3] - 2023-08-15

### Added

- Support for getting completed items through the items archive

## [2.1.2] - 2023-08-14

### Fixes

- Restore Python 3.9 compatibility

## [2.1.1] - 2023-08-09

### Fixes

- Building environment updates

## [2.1.0] - 2023-08-02

### Changed

- Use built-in data classes instead of `attrs`

## [2.0.2] - 2022-11-02

### Fixes

- Task property `date_added` should be `added_at`

## [2.0.1] - 2022-10-06

### Fixes

- Fixed a crash in `get_comments` if attachment is null.

## [2.0.0] - 2022-09-08

Migrate to [REST API v2](https://developer.todoist.com/rest/v2/?python).

## [1.1.1] - 2022-02-15

### Fixes

- Add missing `attrs` package dependency

### Security

- Dependabot updates

## [1.1.0] - 2021-11-23

### Added

- Public release
