import pytest

from cvpysdk.security import __author__


@pytest.mark.unit
class TestSecurityInit:
    """Tests for the security __init__ module."""

    def test_author_is_set(self):
        assert __author__ == "Commvault Systems Inc."
