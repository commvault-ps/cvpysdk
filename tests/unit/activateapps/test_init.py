import pytest

from cvpysdk.activateapps import __author__


@pytest.mark.unit
class TestActivateAppsInit:
    """Tests for the activateapps __init__ module."""

    def test_author_is_set(self):
        assert __author__ == "Commvault Systems Inc."
