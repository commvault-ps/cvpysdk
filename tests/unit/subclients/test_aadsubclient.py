"""Unit tests for cvpysdk/subclients/aadsubclient.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.subclient import Subclient
from cvpysdk.subclients.aadsubclient import AzureAdSubclient


@pytest.mark.unit
class TestAzureAdSubclient:
    """Tests for the AzureAdSubclient class."""

    def test_inherits_subclient(self):
        """AzureAdSubclient should inherit from Subclient."""
        assert issubclass(AzureAdSubclient, Subclient)

    def test_has_restore_in_place_method(self):
        """AzureAdSubclient should have a restore_in_place method."""
        assert hasattr(AzureAdSubclient, "restore_in_place")
        assert callable(AzureAdSubclient.restore_in_place)

    def test_restore_in_place_delegates_to_instance(self):
        """restore_in_place should delegate to instance object's _restore_in_place."""
        subclient = object.__new__(AzureAdSubclient)
        subclient._instance_object = MagicMock()
        subclient._subClientEntity = {"subclientId": 1}
        mock_job = MagicMock()
        subclient._instance_object._restore_in_place.return_value = mock_job

        result = subclient.restore_in_place(some_option="value")

        subclient._instance_object._restore_in_place.assert_called_once_with(some_option="value")
        assert subclient._instance_object._restore_association == subclient._subClientEntity
        assert result == mock_job

    def test_restore_in_place_sets_association(self):
        """restore_in_place should set restore association on instance object."""
        subclient = object.__new__(AzureAdSubclient)
        subclient._instance_object = MagicMock()
        subclient._subClientEntity = {"subclientId": 42}
        subclient._instance_object._restore_in_place.return_value = MagicMock()

        subclient.restore_in_place()

        assert subclient._instance_object._restore_association == {"subclientId": 42}
