"""Unit tests for cvpysdk/subclients/exchange/contentstoremailbox_subclient.py module."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclients.exchange.contentstoremailbox_subclient import (
    ContentStoreMailboxSubclient,
)
from cvpysdk.subclients.exchsubclient import ExchangeSubclient


def _make_backupset_object(mock_commcell):
    """Helper to build a backupset-like mock for exchange subclients."""
    backupset = MagicMock()
    backupset._instance_object = MagicMock()
    backupset._instance_object._agent_object._client_object = MagicMock()
    backupset._instance_object._agent_object._client_object.client_name = "testclient"
    backupset._commcell_object = mock_commcell
    backupset.backupset_id = 10
    return backupset


@pytest.mark.unit
class TestContentStoreMailboxSubclientInheritance:
    """Tests for ContentStoreMailboxSubclient class hierarchy."""

    def test_inherits_exchange_subclient(self):
        assert issubclass(ContentStoreMailboxSubclient, ExchangeSubclient)


@pytest.mark.unit
class TestContentStoreMailboxSubclientGetClientDict:
    """Tests for the static _get_client_dict method."""

    def test_get_client_dict_returns_correct_structure(self):
        client_obj = MagicMock()
        client_obj.client_name = "proxy_client"
        client_obj.client_id = "42"
        result = ContentStoreMailboxSubclient._get_client_dict(client_obj)
        assert result == {"clientName": "proxy_client", "clientId": 42}
