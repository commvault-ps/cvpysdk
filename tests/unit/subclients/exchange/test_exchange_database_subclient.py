"""Unit tests for cvpysdk/subclients/exchange/exchange_database_subclient.py module."""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.exchange.exchange_database_subclient import (
    ExchangeDatabaseSubclient,
)


@pytest.mark.unit
class TestExchangeDatabaseSubclientInheritance:
    """Tests for ExchangeDatabaseSubclient class hierarchy."""

    def test_inherits_subclient(self):
        assert issubclass(ExchangeDatabaseSubclient, Subclient)
