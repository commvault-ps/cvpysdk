import os
from unittest.mock import MagicMock

import pytest

from cvpysdk.services import get_services

BASE_URL = "https://example.com/webconsole/api/"


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
    return get_services(BASE_URL)


@pytest.fixture
def mock_commcell():
    """Commcell-like object with mocked HTTP layer."""
    commcell = MagicMock()
    commcell._services = get_services(BASE_URL)
    commcell._cvpysdk_object = MagicMock()
    commcell._headers = {"Authtoken": "fake-token", "Accept": "application/json"}
    commcell.commserv_name = "testcs"
    commcell.commcell_id = 2
    commcell._web_service = BASE_URL
    commcell.commserv_hostname = "testcs.example.com"
    commcell.commserv_guid = "fake-guid-1234"
    commcell._commcell_object = commcell
    return commcell


@pytest.fixture
def mock_response():
    """Factory for mock HTTP responses."""

    def _make(status_code=200, json_data=None, text=""):
        resp = MagicMock()
        resp.status_code = status_code
        resp.json.return_value = json_data or {}
        resp.text = text
        resp.ok = 200 <= status_code < 300
        return resp

    return _make
