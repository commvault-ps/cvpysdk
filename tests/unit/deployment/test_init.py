"""Unit tests for cvpysdk.deployment.__init__ module."""

import pytest

import cvpysdk.deployment


@pytest.mark.unit
class TestDeploymentInit:
    """Tests for the deployment package initialization."""

    def test_module_has_author(self):
        assert hasattr(cvpysdk.deployment, "__author__")
        assert cvpysdk.deployment.__author__ == "Commvault Systems Inc."

    def test_module_is_importable(self):
        assert cvpysdk.deployment is not None
