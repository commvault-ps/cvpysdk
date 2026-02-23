# Commvault Python SDK

[![Lint](https://github.com/commvault-ps/cvpysdk/actions/workflows/lint.yml/badge.svg)](https://github.com/commvault-ps/cvpysdk/actions/workflows/lint.yml)
[![Tests](https://github.com/commvault-ps/cvpysdk/actions/workflows/test.yml/badge.svg)](https://github.com/commvault-ps/cvpysdk/actions/workflows/test.yml)

This is the Commvault Asia Professional Services (PS) fork of [CVPySDK](https://github.com/Commvault/cvpysdk). The plan is to gradually merge changes here back to the original via Pull Requests.

## Key Enhancements

The following are the key enhancements from the original [CVPySDK](https://github.com/Commvault/cvpysdk):

- **CI/CD**: GitHub Actions workflows for automated:
  - [![Lint](https://github.com/commvault-ps/cvpysdk/actions/workflows/lint.yml/badge.svg)](https://github.com/commvault-ps/cvpysdk/actions/workflows/lint.yml) with [ruff](https://docs.astral.sh/ruff/).
  - [![Testing](https://github.com/commvault-ps/cvpysdk/actions/workflows/test.yml/badge.svg)](https://github.com/commvault-ps/cvpysdk/actions/workflows/test.yml) on Python 3.10, 3.11, 3.12, 3.13, and 3.14 on each [Pull Request](https://github.com/commvault-ps/cvpysdk/pulls) and [branch](https://github.com/commvault-ps/cvpysdk/branches).
- **Build**:
  - Switched from 'pip' → [uv](https://docs.astral.sh/uv/) (which is much faster and simplifies the management of Python virtual environments).
  - Dropped support for old Python versions that are End-Of-Life (EOL):

    | Python Version | EOL Date |
    | --- | --- |
    | 3.6 | December 23, 2021 |
    | 3.7 | June 27, 2023 |
    | 3.8 | October 7, 2024 |
    | 3.9 | October 31, 2025 |

    See <https://endoflife.date/python> for details.

- **Testing**:
  - Initial addition of 1,939 unit tests across 266 modules with shared mock fixtures. This brings unit test coverage from 0.7% to 28%.
  - Fixes to existing integration tests.
- **Code style**:
  - Python code formatting and linting with [Ruff](https://docs.astral.sh/ruff/).
  - Significant auto-fixes and manual fixes.
- **Commit Messages**:
  - Adopt [Commit Convention](<https://www.conventionalcommits.org/en/v1.0.0/>).

- **Docs**:
  - Converted README.rst → [README.md](README.md) with CI badges

## Contribution Guidelines

1. Pull requests to the `main` branch are welcomed!
2. Note that the `main` branch of this repository is based on the `dev` branch of the original [CVPySDK](https://github.com/Commvault/cvpysdk), not `master`.
