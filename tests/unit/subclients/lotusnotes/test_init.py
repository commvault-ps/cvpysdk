"""Unit tests for cvpysdk/subclients/lotusnotes/__init__.py module."""

import pytest


@pytest.mark.unit
class TestLotusNotesSubclientInit:
    """Tests for the lotusnotes subclients package init."""

    def test_module_imports(self):
        """The lotusnotes subclients package should be importable."""
        import cvpysdk.subclients.lotusnotes

        assert hasattr(cvpysdk.subclients.lotusnotes, "__author__")

    def test_author_attribute(self):
        from cvpysdk.subclients.lotusnotes import __author__

        assert __author__ == "Commvault Systems Inc."
