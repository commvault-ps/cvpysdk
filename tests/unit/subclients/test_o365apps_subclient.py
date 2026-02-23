"""Unit tests for cvpysdk/subclients/o365apps_subclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclients.casubclient import CloudAppsSubclient
from cvpysdk.subclients.o365apps_subclient import O365AppsSubclient


@pytest.mark.unit
class TestO365AppsSubclient:
    """Tests for the O365AppsSubclient class."""

    def test_inherits_cloud_apps_subclient(self):
        """O365AppsSubclient should inherit from CloudAppsSubclient."""
        assert issubclass(O365AppsSubclient, CloudAppsSubclient)

    def test_has_key_methods(self):
        """O365AppsSubclient should have expected methods."""
        assert hasattr(O365AppsSubclient, "_prepare_web_search_browse_json")
        assert hasattr(O365AppsSubclient, "_process_web_search_response")
        assert hasattr(O365AppsSubclient, "do_web_search")
        assert hasattr(O365AppsSubclient, "process_index_retention")

    def test_process_web_search_response_success(self):
        """_process_web_search_response should return resultItem on success."""
        sub = object.__new__(O365AppsSubclient)
        mock_response = MagicMock()
        mock_response.json.return_value = {"searchResult": {"resultItem": [{"name": "item1"}]}}
        result = sub._process_web_search_response(True, mock_response)
        assert result == [{"name": "item1"}]

    def test_process_web_search_response_failure_raises(self):
        """_process_web_search_response should raise SDKException on failure."""
        from cvpysdk.exception import SDKException

        sub = object.__new__(O365AppsSubclient)
        sub._update_response_ = MagicMock(return_value="error text")
        mock_response = MagicMock()
        mock_response.text = "error"
        with pytest.raises(SDKException):
            sub._process_web_search_response(False, mock_response)
