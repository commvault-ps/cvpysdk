"""Unit tests for cvpysdk.drorchestration.__init__ module."""

import pytest

import cvpysdk.drorchestration


@pytest.mark.unit
class TestDROrchestrationInit:
    """Tests for the drorchestration package initialization."""

    def test_module_has_author(self):
        assert hasattr(cvpysdk.drorchestration, "__author__")
        assert cvpysdk.drorchestration.__author__ == "Commvault Systems Inc."

    def test_module_is_importable(self):
        assert cvpysdk.drorchestration is not None
