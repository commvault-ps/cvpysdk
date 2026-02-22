import os

import pytest

from cvpysdk.services import get_services


def pytest_collection_modifyitems(config, items):
    """Auto-skip integration tests unless --run-integration or COMMCELL_HOST is set."""
    run_integration = config.getoption("--run-integration", default=False)
    if run_integration or os.environ.get("COMMCELL_HOST"):
        return
    skip_integration = pytest.mark.skip(reason="needs --run-integration or COMMCELL_HOST")
    for item in items:
        if "unit" not in str(item.fspath):
            item.add_marker(skip_integration)


def pytest_addoption(parser):
    parser.addoption(
        "--run-integration",
        action="store_true",
        default=False,
        help="run integration tests requiring live CommCell",
    )


@pytest.fixture
def mock_services():
    return get_services("https://example.com/webconsole/api/")
