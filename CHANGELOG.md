# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

...

## [2.1.3] - [2023-08-15]

### Added

- Support for getting completed items through the items archive

## [2.1.2] - [2023-08-14]

### Fixes

- Restore Python 3.9 compatibility

## [2.1.1] - [2023-08-09]

### Fixes

- Building environment updates

## [2.1.0] - [2023-08-02]

### Changed

- Use built-in data classes instead of `attrs`

## [2.0.2] - [2022-11-02]

### Fixes

- Task property `date_added` should be `added_at`

## [2.0.1] - [2022-10-06]

### Fixes

- Fixed a crash in `get_comments` if attachment is null.

## [2.0.0] - [2022-09-08]

Migrate to [REST API v2](https://developer.todoist.com/rest/v2/?python).

## [1.1.1] - [2022-02-15]

### Fixes

- Add missing `attrs` package dependency

### Security

- Dependabot updates

## [1.1.0] - [2021-11-23]

### Added

- Public release

[1.1.0]: https://github.com/Doist/todoist-api-python/compare/89fe253bd8d92dd88f00a4e8034d43e512b0546f...v1.1.0
[2021-11-23]: https://pypi.org/project/todoist-api-python/1.1.0/
[1.1.1]: https://github.com/Doist/todoist-api-python/compare/v1.1.0...v1.1.1
[2022-02-15]: https://pypi.org/project/todoist-api-python/1.1.1/
[2.0.0]: https://github.com/Doist/todoist-api-python/compare/v1.1.1...v2.0.0
[2022-09-08]: https://pypi.org/project/todoist-api-python/2.0.0/
[2.0.1]: https://github.com/Doist/todoist-api-python/compare/v2.0.0...v2.0.1
[2022-10-06]: https://pypi.org/project/todoist-api-python/2.0.1/
[2.0.2]: https://github.com/Doist/todoist-api-python/compare/v2.0.1...v2.0.2
[2022-11-02]: https://pypi.org/project/todoist-api-python/2.0.2/
[2.1.0]: https://github.com/Doist/todoist-api-python/compare/v2.0.2...v2.1.0
[2023-08-02]: https://pypi.org/project/todoist-api-python/2.1.0/
[2.1.1]: https://github.com/Doist/todoist-api-python/compare/v2.1.0...v2.1.1
[2023-08-09]: https://pypi.org/project/todoist-api-python/2.1.1/
[2.1.2]: https://github.com/Doist/todoist-api-python/compare/v2.1.1...v2.1.2
[2023-08-14]: https://pypi.org/project/todoist-api-python/2.1.2/
[2.1.3]: https://github.com/Doist/todoist-api-python/compare/v2.1.2...v2.1.3
[2023-08-15]: https://pypi.org/project/todoist-api-python/2.1.3/
[Unreleased]: https://github.com/Doist/todoist-api-python/compare/v2.1.3...main
