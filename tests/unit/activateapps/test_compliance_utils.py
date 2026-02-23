from unittest.mock import patch

import pytest

from cvpysdk.activateapps.compliance_utils import (
    ExportSets,
)
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestExportSets:
    """Tests for the ExportSets collection class."""

    def _make_export_sets(self, mock_commcell, sets=None):
        with patch.object(ExportSets, "_get_export_sets", return_value=sets or {}):
            return ExportSets(mock_commcell)

    def test_has_false(self, mock_commcell):
        es = self._make_export_sets(mock_commcell)
        assert es.has("nonexistent") is False

    def test_get_nonexistent_raises(self, mock_commcell):
        es = self._make_export_sets(mock_commcell)
        with pytest.raises(SDKException):
            es.get("nonexistent")

    def test_refresh_calls_get(self, mock_commcell):
        with patch.object(ExportSets, "_get_export_sets", return_value={}) as mock_get:
            es = ExportSets(mock_commcell)
            es.refresh()
        assert mock_get.call_count == 2

    def test_delete_nonexistent_raises(self, mock_commcell):
        es = self._make_export_sets(mock_commcell)
        with pytest.raises(SDKException):
            es.delete("nonexistent")
