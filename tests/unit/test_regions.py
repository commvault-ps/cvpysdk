"""Unit tests for cvpysdk.regions module."""

from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.regions import Region, Regions


@pytest.mark.unit
class TestRegions:
    """Tests for the Regions collection class."""

    def _make_regions(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "regions": [
                    {"name": "USEast", "id": 1},
                    {"name": "EUWest", "id": 2},
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        return Regions(mock_commcell)

    def test_init_populates_regions(self, mock_commcell, mock_response):
        regions = self._make_regions(mock_commcell, mock_response)
        assert "useast" in regions.all_regions
        assert "euwest" in regions.all_regions

    def test_has_region_true(self, mock_commcell, mock_response):
        regions = self._make_regions(mock_commcell, mock_response)
        assert regions.has_region("USEast") is True

    def test_has_region_false(self, mock_commcell, mock_response):
        regions = self._make_regions(mock_commcell, mock_response)
        assert regions.has_region("nonexistent") is False

    def test_get_returns_region_object(self, mock_commcell, mock_response):
        regions = self._make_regions(mock_commcell, mock_response)
        with patch.object(Region, "__init__", return_value=None):
            result = regions.get("USEast")
            assert isinstance(result, Region)

    def test_get_raises_on_missing(self, mock_commcell, mock_response):
        regions = self._make_regions(mock_commcell, mock_response)
        with pytest.raises(SDKException):
            regions.get("nonexistent")

    def test_refresh(self, mock_commcell, mock_response):
        regions = self._make_regions(mock_commcell, mock_response)
        resp2 = mock_response(
            json_data={
                "regions": [
                    {"name": "APSouth", "id": 3},
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp2)
        regions.refresh()
        assert "apsouth" in regions.all_regions
        assert "useast" not in regions.all_regions

    def test_init_raises_on_empty_response(self, mock_commcell, mock_response):
        resp = mock_response(json_data={})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        with pytest.raises(SDKException):
            Regions(mock_commcell)

    def test_duplicate_names_with_different_companies(self, mock_commcell, mock_response):
        resp = mock_response(
            json_data={
                "regions": [
                    {
                        "name": "Default",
                        "id": 1,
                        "company": {"name": "CompanyA"},
                    },
                    {
                        "name": "Default",
                        "id": 2,
                        "company": {"name": "CompanyB"},
                    },
                ]
            }
        )
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        regions = Regions(mock_commcell)
        # With duplicate names, keys should include company suffix
        assert "default_(companya)" in regions.all_regions
        assert "default_(companyb)" in regions.all_regions
