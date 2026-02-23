"""Unit tests for cvpysdk.agents.__init__ module."""

import pytest


@pytest.mark.unit
class TestAgentsInit:
    """Tests for the agents package __init__."""

    def test_import_agents_package(self):
        """Test that the agents package is importable."""
        import cvpysdk.agents

        assert hasattr(cvpysdk.agents, "__author__")

    def test_author_attribute(self):
        """Test __author__ is set correctly."""
        from cvpysdk.agents import __author__

        assert __author__ == "Commvault Systems Inc."
