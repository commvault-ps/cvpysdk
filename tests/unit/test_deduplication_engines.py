from unittest.mock import patch

import pytest

from cvpysdk.deduplication_engines import DeduplicationEngine, DeduplicationEngines
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestDeduplicationEngines:
    """Tests for the DeduplicationEngines collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(DeduplicationEngines, "_get_engines", return_value={}):
            de = DeduplicationEngines(mock_commcell)
        assert "DeduplicationEngines" in repr(de)

    def test_all_engines_property_empty(self, mock_commcell):
        with patch.object(DeduplicationEngines, "_get_engines", return_value={}):
            de = DeduplicationEngines(mock_commcell)
        assert de.all_engines == []

    def test_all_engines_property_with_data(self, mock_commcell):
        engines = {("sp1", "copy1"): ["1", "2"]}
        with patch.object(DeduplicationEngines, "_get_engines", return_value=engines):
            de = DeduplicationEngines(mock_commcell)
        assert de.all_engines == [("sp1", "copy1")]

    def test_has_engine_true(self, mock_commcell):
        engines = {("sp1", "copy1"): ["1", "2"]}
        with patch.object(DeduplicationEngines, "_get_engines", return_value=engines):
            de = DeduplicationEngines(mock_commcell)
            assert de.has_engine("sp1", "copy1") is True

    def test_has_engine_false(self, mock_commcell):
        engines = {("sp1", "copy1"): ["1", "2"]}
        with patch.object(DeduplicationEngines, "_get_engines", return_value=engines):
            de = DeduplicationEngines(mock_commcell)
            assert not de.has_engine("sp2", "copy2")

    def test_get_nonexistent_raises(self, mock_commcell):
        with patch.object(DeduplicationEngines, "_get_engines", return_value={}):
            de = DeduplicationEngines(mock_commcell)
            with pytest.raises(SDKException):
                de.get("nonexistent_sp", "nonexistent_copy")

    def test_str_representation(self, mock_commcell):
        engines = {("sp1", "copy1"): ["1", "2"]}
        with patch.object(DeduplicationEngines, "_get_engines", return_value=engines):
            de = DeduplicationEngines(mock_commcell)
        result = str(de)
        assert "sp1/copy1" in result

    def test_refresh(self, mock_commcell):
        with patch.object(DeduplicationEngines, "_get_engines", return_value={}) as mock_get:
            de = DeduplicationEngines(mock_commcell)
            de.refresh()
        assert mock_get.call_count == 2


@pytest.mark.unit
class TestDeduplicationEngine:
    """Tests for the DeduplicationEngine entity class."""

    def test_repr(self, mock_commcell):
        with patch.object(DeduplicationEngine, "_initialize_policy_and_copy_id"), patch.object(
            DeduplicationEngine, "_initialize_engine_properties"
        ), patch.object(DeduplicationEngine, "_initialize_stores"):
            engine = DeduplicationEngine.__new__(DeduplicationEngine)
            engine._storage_policy_name = "sp1"
            engine._copy_name = "copy1"
            engine._commcell_object = mock_commcell
        assert "sp1/copy1" in repr(engine)
