"""Unit tests for cvpysdk/subclients/splunksubclient.py"""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.subclients.bigdataappssubclient import BigDataAppsSubclient
from cvpysdk.subclients.splunksubclient import SplunkSubclient


@pytest.mark.unit
class TestSplunkSubclient:
    """Tests for the SplunkSubclient class."""

    def test_inherits_big_data_apps_subclient(self):
        """SplunkSubclient should inherit from BigDataAppsSubclient."""
        assert issubclass(SplunkSubclient, BigDataAppsSubclient)

    def test_has_key_methods(self):
        """SplunkSubclient should have expected methods."""
        assert hasattr(SplunkSubclient, "restore_in_place")
        assert hasattr(SplunkSubclient, "subclient_content")

    def test_subclient_content_property(self):
        """subclient_content should return list of index titles."""
        sub = object.__new__(SplunkSubclient)
        sub._subclient_properties = {}
        sub._properties = {
            "splunkProps": {
                "contentList": [
                    {"title": "index1"},
                    {"title": "index2"},
                ]
            }
        }
        # Use the properties dict directly since we bypass __init__
        with patch.object(
            type(sub), "properties", new_callable=lambda: property(lambda self: self._properties)
        ):
            result = sub.subclient_content
            assert result == ["index1", "index2"]

    def test_subclient_content_setter_updates_properties(self):
        """subclient_content setter should build proper content list."""
        sub = object.__new__(SplunkSubclient)
        sub._properties = {
            "splunkProps": {
                "contentList": [
                    {"title": "old_index", "path": "indexes/old_index", "level": 1, "type": 1}
                ]
            }
        }
        sub.update_properties = MagicMock()
        with patch.object(
            type(sub), "properties", new_callable=lambda: property(lambda self: self._properties)
        ):
            sub.subclient_content = ["new_idx1", "new_idx2"]
            sub.update_properties.assert_called_once()
