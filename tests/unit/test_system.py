"""Unit tests for cvpysdk/system.py module."""

import pytest

from cvpysdk.system import System


@pytest.mark.unit
class TestSystem:
    """Tests for the System class."""

    def test_init_stores_commcell(self, mock_commcell):
        system = System(mock_commcell)
        assert system._commcell_object is mock_commcell

    def test_set_gui_timeout_calls_set_gxglobalparam(self, mock_commcell):
        system = System(mock_commcell)
        system.set_gui_timeout(30)
        mock_commcell._set_gxglobalparam_value.assert_called_once_with(
            {"name": "Gui timeout", "value": "30"}
        )

    def test_set_gui_timeout_zero_disables(self, mock_commcell):
        system = System(mock_commcell)
        system.set_gui_timeout(0)
        mock_commcell._set_gxglobalparam_value.assert_called_once_with(
            {"name": "Gui timeout", "value": "0"}
        )
