"""Unit tests for cvpysdk.commcell_migration module."""

import pytest

from cvpysdk.commcell_migration import CommCellMigration


@pytest.mark.unit
class TestCommCellMigration:
    """Tests for the CommCellMigration class."""

    def test_init(self, mock_commcell):
        ccm = CommCellMigration(mock_commcell)
        assert ccm._commcell_object is mock_commcell
        assert ccm._commcell_name == "testcs"
        assert ccm._path_type == 0

    def test_init_sets_services(self, mock_commcell):
        ccm = CommCellMigration(mock_commcell)
        assert ccm._services is mock_commcell._services
        assert ccm._cvpysdk_object is mock_commcell._cvpysdk_object
