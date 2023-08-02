# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

...

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
