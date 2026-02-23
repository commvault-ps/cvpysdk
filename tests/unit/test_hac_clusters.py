"""Unit tests for cvpysdk.hac_clusters module."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.hac_clusters import HACClusters


@pytest.mark.unit
class TestHACClusters:
    """Tests for the HACClusters collection class."""

    def _make_clusters(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "nodeClientGroupInfo": [
                    {
                        "nodeGroupType": 3,
                        "clientGroup": {
                            "clientGroupName": "TestCluster",
                            "clientGroupId": 10,
                        },
                    }
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_commcell.clients = MagicMock()
        mock_commcell.clients.refresh = MagicMock()
        mock_commcell.client_groups = MagicMock()
        mock_commcell.client_groups.refresh = MagicMock()
        return HACClusters(mock_commcell)

    def test_init_populates_clusters(self, mock_commcell, mock_response):
        clusters = self._make_clusters(mock_commcell, mock_response)
        assert clusters.all_hac_clusters is not None

    def test_has_cluster_false(self, mock_commcell, mock_response):
        clusters = self._make_clusters(mock_commcell, mock_response)
        assert clusters.has_cluster("nonexistent") is False

    def test_has_cluster_raises_on_non_string(self, mock_commcell, mock_response):
        clusters = self._make_clusters(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            clusters.has_cluster(123)

    def test_repr(self, mock_commcell, mock_response):
        clusters = self._make_clusters(mock_commcell, mock_response)
        assert "HACClusters" in repr(clusters)
