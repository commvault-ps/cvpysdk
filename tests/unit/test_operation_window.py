"""Unit tests for cvpysdk.operation_window module."""

from unittest.mock import patch

import pytest

from cvpysdk.operation_window import OperationWindow


@pytest.mark.unit
class TestOperationWindow:
    """Tests for the OperationWindow class."""

    def _make_op_window(self, mock_commcell):
        """Create an OperationWindow instance backed by a mock Commcell."""
        with patch("cvpysdk.operation_window.isinstance") as mock_isinstance:
            # Force isinstance to match Commcell path
            mock_isinstance.side_effect = lambda obj, cls: (
                cls.__name__ == "Commcell" if hasattr(cls, "__name__") else False
            )
            ow = OperationWindow.__new__(OperationWindow)
            ow._commcell_object = mock_commcell
            ow._cvpysdk_object = mock_commcell._cvpysdk_object
            ow._services = mock_commcell._services
            ow._entity_type_id = 0
            ow._entity_id = 0
            ow._commcell_id = mock_commcell.commcell_id
            ow._clientgroup_id = 0
            ow._client_id = 0
            ow._agent_id = 0
            ow._instance_id = 0
            ow._backupset_id = 0
            ow._subclient_id = 0
            ow._entity_level = "commcell"
            return ow

    def test_entity_level_is_commcell(self, mock_commcell):
        ow = self._make_op_window(mock_commcell)
        assert ow._entity_level == "commcell"
