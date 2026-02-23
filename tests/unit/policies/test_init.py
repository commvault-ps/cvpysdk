import pytest

from cvpysdk.policies import __author__


@pytest.mark.unit
class TestPoliciesInit:
    """Tests for the policies __init__ module."""

    def test_author_is_set(self):
        assert __author__ == "Commvault Systems Inc."
