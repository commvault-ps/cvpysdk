"""Unit tests for cvpysdk/subclients/exchsubclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.exchsubclient import ExchangeSubclient


@pytest.mark.unit
class TestExchangeSubclient:
    """Tests for the ExchangeSubclient class."""

    def test_inherits_subclient(self):
        """ExchangeSubclient should inherit from Subclient."""
        assert issubclass(ExchangeSubclient, Subclient)

    def test_has_key_methods(self):
        """ExchangeSubclient should have expected methods."""
        assert hasattr(ExchangeSubclient, "restore_in_place")
        assert hasattr(ExchangeSubclient, "out_of_place_restore")
        assert hasattr(ExchangeSubclient, "disk_restore")
        assert hasattr(ExchangeSubclient, "pst_restore")
        assert hasattr(ExchangeSubclient, "cleanup")
        assert hasattr(ExchangeSubclient, "subclient_content_indexing")
        assert hasattr(ExchangeSubclient, "pst_ingestion")
        assert hasattr(ExchangeSubclient, "ad_group_backup")

    def test_new_user_mailbox(self):
        """__new__ should return UsermailboxSubclient for 'user mailbox' backupset."""
        from cvpysdk.subclients.exchange.usermailbox_subclient import (
            UsermailboxSubclient,
        )

        backupset_obj = MagicMock()
        backupset_obj.backupset_name = "user mailbox"
        result = ExchangeSubclient.__new__(ExchangeSubclient, backupset_obj, "test")
        assert isinstance(result, UsermailboxSubclient)

    def test_new_journal_mailbox(self):
        """__new__ should return JournalMailboxSubclient for 'journal mailbox'."""
        from cvpysdk.subclients.exchange.journalmailbox_subclient import (
            JournalMailboxSubclient,
        )

        backupset_obj = MagicMock()
        backupset_obj.backupset_name = "journal mailbox"
        result = ExchangeSubclient.__new__(ExchangeSubclient, backupset_obj, "test")
        assert isinstance(result, JournalMailboxSubclient)

    def test_new_raises_for_unknown_backupset(self):
        """__new__ should raise SDKException for unknown backupset name."""
        from cvpysdk.exception import SDKException

        backupset_obj = MagicMock()
        backupset_obj.backupset_name = "unknown_backupset"
        with pytest.raises(SDKException):
            ExchangeSubclient.__new__(ExchangeSubclient, backupset_obj, "test")

    def test_get_client_dict_static_method(self):
        """_get_client_dict should return properly formatted client dict."""
        client_obj = MagicMock()
        client_obj.client_name = "test_client"
        client_obj.client_id = 42
        result = ExchangeSubclient._get_client_dict(client_obj)
        assert result["client"]["clientName"] == "test_client"
        assert result["client"]["clientId"] == 42
        assert result["client"]["_type_"] == 3

    def test_restore_in_place_raises_for_empty_paths(self):
        """restore_in_place should raise SDKException for empty paths."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(ExchangeSubclient)
        with pytest.raises(SDKException):
            subclient.restore_in_place(paths=[])

    def test_get_ad_group_backup_common_opt_json(self):
        """_get_ad_group_backup_common_opt_json should return correct format."""
        result = ExchangeSubclient._get_ad_group_backup_common_opt_json("TestGroup")
        assert result["notifyUserOnJobCompletion"] is False
        assert result["jobMetadata"][0]["selectedItems"][0]["itemName"] == "TestGroup"
        assert result["jobMetadata"][0]["selectedItems"][0]["itemType"] == "AD group"
