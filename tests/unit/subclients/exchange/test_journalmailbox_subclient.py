"""Unit tests for cvpysdk/subclients/exchange/journalmailbox_subclient.py module."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclients.exchange.journalmailbox_subclient import (
    JournalMailboxSubclient,
)
from cvpysdk.subclients.exchsubclient import ExchangeSubclient


def _make_backupset_object(mock_commcell):
    """Helper to build a backupset-like mock for journal subclient."""
    backupset = MagicMock()
    backupset._instance_object = MagicMock()
    backupset._instance_object._agent_object._client_object = MagicMock()
    backupset._commcell_object = mock_commcell
    backupset.backupset_id = 10
    return backupset


@pytest.mark.unit
class TestJournalMailboxSubclientInheritance:
    """Tests for JournalMailboxSubclient class hierarchy."""

    def test_inherits_exchange_subclient(self):
        assert issubclass(JournalMailboxSubclient, ExchangeSubclient)
