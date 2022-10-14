# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

* Added Support for testing in Python 3.9 and 3.10
* Add Python 3.10 support to the PythonVersion constants and pyproject.toml python_versions
* Update workflow testing version to python 3.10.7

## [0.2.1] - 2021-10-21

### Fixed

* Bug preventing Python binaries from being looked up
* Bug requiring that python versions be provided in UPPER_SNAKE_CASE (CP38_CP38)

## [0.2.0] - 2021-10-01

### Changed

* Uppercase Enum keys
* Expand `click` version range to `click>=7.1,<9`

## [0.1.0] - 2021-02-18

Initial release
