"""Unit tests for cvpysdk/subclients/exchange/__init__.py module."""

import pytest


@pytest.mark.unit
class TestExchangeSubclientInit:
    """Tests for the exchange subclients package init."""

    def test_module_imports(self):
        """The exchange subclients package should be importable."""
        import cvpysdk.subclients.exchange

        assert hasattr(cvpysdk.subclients.exchange, "__author__")

    def test_author_attribute(self):
        from cvpysdk.subclients.exchange import __author__

        assert __author__ == "Commvault Systems Inc."
