"""Unit tests for cvpysdk.name_change module."""

from unittest.mock import MagicMock

import pytest

from cvpysdk.name_change import NameChange, OperationType


@pytest.mark.unit
class TestOperationType:
    """Tests for the OperationType enum."""

    def test_commserver_hostname_remote_clients_value(self):
        assert OperationType.COMMSERVER_HOSTNAME_REMOTE_CLIENTS.value == 147

    def test_commserver_hostname_after_dr_value(self):
        assert OperationType.COMMSERVER_HOSTNAME_AFTER_DR.value == 139

    def test_client_hostname_value(self):
        assert OperationType.CLIENT_HOSTNAME.value == "CLIENT_HOSTNAME"

    def test_commserver_hostname_value(self):
        assert OperationType.COMMSERVER_HOSTNAME.value == "COMMSERVER_HOSTNAME"


@pytest.mark.unit
class TestNameChange:
    """Tests for the NameChange class."""

    def _make_client_name_change(self, mock_commcell):
        """Create a NameChange instance for a client."""
        nc = NameChange.__new__(NameChange)
        nc._commcell_object = mock_commcell
        nc._cvpysdk_object = mock_commcell._cvpysdk_object
        nc._services = mock_commcell._services
        nc._update_response_ = mock_commcell._update_response_
        nc._is_client = True
        nc._client_hostname = "testhost"
        nc._display_name = "Test Display"
        nc._client_name = "testclient"
        nc._commcell_name = "testcs"
        nc._new_name = None
        nc._client_object = MagicMock()
        nc._client_object._cvpysdk_object = mock_commcell._cvpysdk_object
        return nc

    def _make_commcell_name_change(self, mock_commcell):
        """Create a NameChange instance for a commcell."""
        nc = NameChange.__new__(NameChange)
        nc._commcell_object = mock_commcell
        nc._cvpysdk_object = mock_commcell._cvpysdk_object
        nc._services = mock_commcell._services
        nc._update_response_ = mock_commcell._update_response_
        nc._is_client = False
        nc._display_name = "CS Display"
        nc._commcell_name = "testcs"
        return nc

    def test_hostname_getter_client(self, mock_commcell):
        nc = self._make_client_name_change(mock_commcell)
        assert nc.hostname == "testhost"

    def test_hostname_getter_commcell(self, mock_commcell):
        nc = self._make_commcell_name_change(mock_commcell)
        assert nc.hostname == "testcs"

    def test_display_name_getter_client(self, mock_commcell):
        nc = self._make_client_name_change(mock_commcell)
        assert nc.display_name == "Test Display"

    def test_display_name_getter_commcell(self, mock_commcell):
        nc = self._make_commcell_name_change(mock_commcell)
        assert nc.display_name == "CS Display"

    def test_client_name_getter(self, mock_commcell):
        nc = self._make_client_name_change(mock_commcell)
        assert nc.client_name == "testclient"

    def test_domain_name_getter(self, mock_commcell):
        nc = self._make_commcell_name_change(mock_commcell)
        assert nc.domain_name == "testcs"
