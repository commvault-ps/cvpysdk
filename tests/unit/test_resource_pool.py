"""Unit tests for cvpysdk.resource_pool module."""

from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.resource_pool import ResourcePool, ResourcePools, ResourcePoolTypes


@pytest.mark.unit
class TestResourcePoolTypes:
    """Tests for the ResourcePoolTypes enum."""

    def test_generic_value(self):
        assert ResourcePoolTypes.GENERIC.value == 0

    def test_o365_value(self):
        assert ResourcePoolTypes.O365.value == 1

    def test_threatscan_value(self):
        assert ResourcePoolTypes.THREATSCAN.value == 22

    def test_gcp_value(self):
        assert ResourcePoolTypes.GOOGLE_CLOUD_PLATFORM.value == 50001


@pytest.mark.unit
class TestResourcePools:
    """Tests for the ResourcePools collection class."""

    def _make_pools(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "resourcePools": [
                    {"name": "TestPool", "id": 1, "appType": 22},
                    {"name": "OtherPool", "id": 2, "appType": 8},
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return ResourcePools(mock_commcell)

    def test_init_populates_pools(self, mock_commcell, mock_response):
        pools = self._make_pools(mock_commcell, mock_response)
        assert "testpool" in pools._pools
        assert "otherpool" in pools._pools

    def test_has_true(self, mock_commcell, mock_response):
        pools = self._make_pools(mock_commcell, mock_response)
        assert pools.has("TestPool") is True

    def test_has_false(self, mock_commcell, mock_response):
        pools = self._make_pools(mock_commcell, mock_response)
        assert pools.has("missing") is False

    def test_get_returns_resource_pool_object(self, mock_commcell, mock_response):
        pools = self._make_pools(mock_commcell, mock_response)
        with patch.object(ResourcePool, "__init__", return_value=None):
            result = pools.get("TestPool")
            assert isinstance(result, ResourcePool)

    def test_get_raises_on_missing(self, mock_commcell, mock_response):
        pools = self._make_pools(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            pools.get("nonexistent")

    def test_refresh(self, mock_commcell, mock_response):
        pools = self._make_pools(mock_commcell, mock_response)
        resp2 = mock_response(
            json_data={
                "resourcePools": [
                    {"name": "NewPool", "id": 3, "appType": 1},
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp2)
        pools.refresh()
        assert "newpool" in pools._pools
        assert "testpool" not in pools._pools

    def test_empty_response(self, mock_commcell, mock_response):
        resp = mock_response(json_data={})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        pools = ResourcePools(mock_commcell)
        assert pools._pools == {}
