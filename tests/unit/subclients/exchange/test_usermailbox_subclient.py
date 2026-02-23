"""Unit tests for cvpysdk/subclients/exchange/usermailbox_subclient.py module."""

import pytest

from cvpysdk.subclients.exchange.usermailbox_subclient import UsermailboxSubclient
from cvpysdk.subclients.exchsubclient import ExchangeSubclient


@pytest.mark.unit
class TestUsermailboxSubclientInheritance:
    """Tests for UsermailboxSubclient class hierarchy."""

    def test_inherits_exchange_subclient(self):
        assert issubclass(UsermailboxSubclient, ExchangeSubclient)


@pytest.mark.unit
class TestUsermailboxSubclientFindMailboxHelpers:
    """Tests for static helper methods."""

    def test_find_mailbox_query_params_default(self):
        result = UsermailboxSubclient._find_mailbox_query_params()
        assert isinstance(result, list)
        param_names = [p["param"] for p in result]
        assert "RESPONSE_FIELD_LIST" in param_names
        assert "SHOW_EMAILS_ONLY" in param_names

    def test_find_mailbox_facets_with_defaults(self):
        result = UsermailboxSubclient._find_mailbox_facets(facets=["MODIFIEDTIME"])
        assert isinstance(result, list)
        facet_names = [f["name"] for f in result]
        assert "MODIFIEDTIME" in facet_names
