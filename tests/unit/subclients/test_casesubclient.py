"""Unit tests for cvpysdk/subclients/casesubclient.py"""

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.casesubclient import CaseSubclient


@pytest.mark.unit
class TestCaseSubclient:
    """Tests for the CaseSubclient class."""

    def test_inherits_subclient(self):
        """CaseSubclient should inherit from Subclient."""
        assert issubclass(CaseSubclient, Subclient)

    def test_has_key_methods(self):
        """CaseSubclient should have expected methods."""
        assert hasattr(CaseSubclient, "index_copy")
        assert hasattr(CaseSubclient, "data_copy")
        assert hasattr(CaseSubclient, "content_indexing")
        assert hasattr(CaseSubclient, "add_definition")
        assert hasattr(CaseSubclient, "_case_definition_request")

    def test_json_search_request_property(self):
        """json_search_request should return the search request JSON."""
        subclient = object.__new__(CaseSubclient)
        subclient._filter_list = [{"interGroupOP": 2, "filter": {}}]

        result = subclient.json_search_request
        assert "advSearchGrp" in result
        assert "searchProcessingInfo" in result

    def test_json_index_copy_options(self):
        """json_index_copy_options should return admin options with type=1."""
        subclient = object.__new__(CaseSubclient)
        result = subclient.json_index_copy_options
        assert result["adminOpts"]["caseMgrOptions"]["type"] == 1

    def test_json_data_copy_subtasks(self):
        """json_data_copy_subtasks should return subtask with operationType=2."""
        subclient = object.__new__(CaseSubclient)
        result = subclient.json_data_copy_subtasks
        assert result["subTaskType"] == 2
        assert result["operationType"] == 2

    def test_json_data_copy_options(self):
        """json_data_copy_options should return backup opts with type=2."""
        subclient = object.__new__(CaseSubclient)
        result = subclient.json_data_copy_options
        assert result["backupOpts"]["caseMgrOptions"]["type"] == 2

    def test_add_definition_raises_for_non_list_custodian(self):
        """add_definition should raise SDKException if custodian_info is not a list."""
        from cvpysdk.exception import SDKException

        subclient = object.__new__(CaseSubclient)
        with pytest.raises(SDKException):
            subclient.add_definition("test_def", "not_a_list")
