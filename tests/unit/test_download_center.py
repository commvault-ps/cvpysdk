from unittest.mock import patch

import pytest

from cvpysdk.download_center import DownloadCenter


@pytest.mark.unit
class TestDownloadCenter:
    """Tests for the DownloadCenter class."""

    def test_repr(self, mock_commcell):
        with patch.object(DownloadCenter, "_get_properties"), patch.object(
            DownloadCenter, "_get_packages"
        ):
            dc = DownloadCenter(mock_commcell)
        assert "DownloadCenter" in repr(dc)

    def test_init_sets_attributes(self, mock_commcell):
        with patch.object(DownloadCenter, "_get_properties"), patch.object(
            DownloadCenter, "_get_packages"
        ):
            dc = DownloadCenter(mock_commcell)
        assert dc._commcell_object is mock_commcell

    def test_refresh_calls_methods(self, mock_commcell):
        with patch.object(DownloadCenter, "_get_properties") as mock_props, patch.object(
            DownloadCenter, "_get_packages"
        ) as mock_pkgs:
            dc = DownloadCenter(mock_commcell)
            dc.refresh()
        # refresh is called once in __init__ and once explicitly
        assert mock_props.call_count == 2
        assert mock_pkgs.call_count == 2
