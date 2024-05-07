# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

...

## [2.1.4] - 2024-05-07

### What's Changed
* chore(deps): update python docker tag to v3.11.5 by @renovate in https://github.com/Doist/todoist-api-python/pull/107
* chore: Update actions to support NodeJS 20 by @deorus in https://github.com/Doist/todoist-api-python/pull/113
* Bump certifi from 2022.6.15 to 2023.7.22 by @dependabot in https://github.com/Doist/todoist-api-python/pull/114
* Bump urllib3 from 1.26.12 to 1.26.17 by @dependabot in https://github.com/Doist/todoist-api-python/pull/117
* Bump urllib3 from 1.26.17 to 1.26.18 by @dependabot in https://github.com/Doist/todoist-api-python/pull/120
* build: Switch to poetry-core by @lefcha in https://github.com/Doist/todoist-api-python/pull/121
* chore: Migrate to Ruff by @lefcha in https://github.com/Doist/todoist-api-python/pull/127
* Bump idna from 3.3 to 3.7 by @dependabot in https://github.com/Doist/todoist-api-python/pull/133
* feat: Support project.can_assign_tasks by @amix in https://github.com/Doist/todoist-api-python/pull/132
* feat: add duration to Task object by @eitchtee in https://github.com/Doist/todoist-api-python/pull/109
* docs: pagination example by @iloveitaly in https://github.com/Doist/todoist-api-python/pull/126
* chore(deps): update python docker tag to v3.12.3 by @renovate in https://github.com/Doist/todoist-api-python/pull/119

### New Contributors
* @deorus made their first contribution in https://github.com/Doist/todoist-api-python/pull/113
* @amix made their first contribution in https://github.com/Doist/todoist-api-python/pull/132
* @eitchtee made their first contribution in https://github.com/Doist/todoist-api-python/pull/109
* @iloveitaly made their first contribution in https://github.com/Doist/todoist-api-python/pull/126

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
