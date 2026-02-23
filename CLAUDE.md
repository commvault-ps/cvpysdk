# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

CVPySDK is a Python SDK (v11.42) for Commvault Software that wraps Commvault REST APIs into a Pythonic object model. It supports Python 3.10+ and requires a Commvault CommCell with WebConsole installed.

## Build and Install

```bash
uv sync --extra dev                # Development install (with dev dependencies)
uv pip install cvpysdk             # From PyPI
python setup.py install             # Legacy install
```

Dependencies: `requests`, `xmltodict`, `pycryptodomex`

## Testing

Tests require a live Commvault CommCell. Configure `tests/input.json` with credentials before running:

```bash
python tests/test_all.py            # Run all tests (unittest discovery)
python -m pytest tests/test_client.py  # Run a single test file
```

Tests use `unittest` (or `unittest2` fallback). The base class `SDKTestCase` in `tests/testlib.py` reads CommCell credentials from `tests/input.json` and creates/tears down a Commcell connection per test.

## Commits

All commits MUST follow [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

Format: `<type>[optional scope]: <description>`

Allowed types: `feat`, `fix`, `docs`, `style`, `refactor`, `perf`, `test`, `build`, `ci`, `chore`, `revert`

- Use lowercase type and description
- Do not end the description with a period
- Use `!` after type/scope for breaking changes (e.g., `feat!: remove deprecated API`)
- Add optional body/footer separated by blank lines for additional context
- Do NOT include a `Co-Authored-By` trailer in commit messages

Examples:
- `feat(client): add backup scheduling support`
- `fix: handle token expiry during long-running jobs`
- `docs: update CLAUDE.md with commit conventions`

## Code Style

- PEP8 with **line-length=99** (not the default 79)
- Lint with `ruff check .` and auto-fix with `ruff check --fix .`
- Format with `ruff format .` (or check formatting with `ruff format --check .`)
- Legacy: `autopep8 --max-line-length=99` is also accepted
- Inline pylint disables are used where needed (e.g., `# pylint: disable=R1705`)
- Pre-commit hook: run `pre-commit install` to enable automatic linting on commit

## Architecture

### Entity Hierarchy

The SDK mirrors Commvault's entity hierarchy. Each level has a **collection class** (plural) and an **entity class** (singular):

```
Commcell (commcell.py) — entry point, aggregates all subsystems
├── Clients / Client (client.py)
│   └── Agents / Agent (agent.py)
│       ├── Instances / Instance (instance.py)
│       │   └── Backupsets / Backupset (backupset.py)
│       │       └── Subclients / Subclient (subclient.py)
│       └── Backupsets / Backupset
│           └── Subclients / Subclient
└── Global entities: Jobs, Plans, Storage, Organizations, Security, etc.
```

Collection classes (e.g., `Clients`) handle listing, adding, and deleting entities. Entity classes (e.g., `Client`) represent individual instances with properties and operations.

### Key Layers

1. **Session layer** (`cvpysdk.py`): `CVPySDK` class handles authentication, HTTP requests (GET/POST/PUT/DELETE), token renewal, and SSL
2. **Orchestration layer** (`commcell.py`): `Commcell` class is the main entry point — it aggregates ~60+ properties for all subsystems
3. **REST endpoints** (`services.py`): `SERVICES_DICT_TEMPLATE` maps symbolic names to URL patterns. New endpoints are added here as `"{0}endpoint/path"`
4. **Error handling** (`exception.py`): `SDKException(module, id, message)` with error codes defined in `EXCEPTION_DICT` keyed by module name

### Agent-Specific Extensions

Agent-specific behaviors are implemented via subclasses in subdirectories:

- `cvpysdk/subclients/` — Agent-specific subclient implementations (e.g., `fssubclient.py` for File System, `vssubclient.py` for Virtual Server)
- `cvpysdk/instances/` — Agent-specific instance implementations (e.g., `oracleinstance.py`, `mysqlinstance.py`)
- Additional agent modules: `cvpysdk/virtualserver/`, `cvpysdk/exchange/`, `cvpysdk/cloudapps/`, `cvpysdk/security/`

### Common Patterns

- **Lazy loading**: Properties fetch data from the REST API on first access
- **Context manager**: `Commcell` supports `with` for automatic logout
- **`_update_response_()`**: Methods on entity classes that normalize API responses
- **`refresh()` method**: Forces re-fetch of entity properties from the API

### Adding New Features

- **New REST endpoint**: Add key/URL to `SERVICES_DICT_TEMPLATE` in `services.py`
- **New exception**: Add module key and error codes to `EXCEPTION_DICT` in `exception.py`
- **New agent type**: Create subclass files in `subclients/` and/or `instances/`, following the pattern of existing implementations
