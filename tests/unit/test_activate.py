"""Unit tests for cvpysdk/activate.py module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.activate import Activate
from cvpysdk.activateapps.entity_manager import EntityManagerTypes
from cvpysdk.activateapps.file_storage_optimization import FsoTypes
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestActivateInit:
    """Tests for the Activate class constructor."""

    def test_init_stores_commcell(self, mock_commcell):
        activate = Activate(mock_commcell)
        assert activate._commcell_object is mock_commcell

    def test_init_lazy_attrs_are_none(self, mock_commcell):
        activate = Activate(mock_commcell)
        assert activate._entity is None
        assert activate._tags is None
        assert activate._classifiers is None
        assert activate._inventories is None
        assert activate._fso_servers is None
        assert activate._fso_server_groups is None
        assert activate._sdg_projects is None
        assert activate._req_mgr is None
        assert activate._compliance_search is None


@pytest.mark.unit
class TestActivateInventoryManager:
    """Tests for Activate.inventory_manager."""

    def test_inventory_manager_lazy_init(self, mock_commcell):
        activate = Activate(mock_commcell)
        with patch("cvpysdk.activate.Inventories") as MockInv:
            MockInv.return_value = MagicMock()
            result = activate.inventory_manager()
            MockInv.assert_called_once_with(mock_commcell)
            assert result is not None

    def test_inventory_manager_cached(self, mock_commcell):
        activate = Activate(mock_commcell)
        with patch("cvpysdk.activate.Inventories") as MockInv:
            mock_instance = MagicMock()
            MockInv.return_value = mock_instance
            result1 = activate.inventory_manager()
            result2 = activate.inventory_manager()
            MockInv.assert_called_once()
            assert result1 is result2


@pytest.mark.unit
class TestActivateRequestManager:
    """Tests for Activate.request_manager."""

    def test_request_manager_lazy_init(self, mock_commcell):
        activate = Activate(mock_commcell)
        with patch("cvpysdk.activate.Requests") as MockReq:
            MockReq.return_value = MagicMock()
            result = activate.request_manager()
            MockReq.assert_called_once_with(mock_commcell)
            assert result is not None


@pytest.mark.unit
class TestActivateEntityManager:
    """Tests for Activate.entity_manager."""

    def test_entity_manager_default_type(self, mock_commcell):
        activate = Activate(mock_commcell)
        with patch("cvpysdk.activate.ActivateEntities") as MockEntities:
            MockEntities.return_value = MagicMock()
            result = activate.entity_manager()
            MockEntities.assert_called_once_with(mock_commcell)
            assert result is not None

    def test_entity_manager_bad_type_raises(self, mock_commcell):
        activate = Activate(mock_commcell)
        with pytest.raises(SDKException):
            activate.entity_manager(entity_type="invalid")

    def test_entity_manager_tags_type(self, mock_commcell):
        activate = Activate(mock_commcell)
        with patch("cvpysdk.activate.Tags") as MockTags:
            MockTags.return_value = MagicMock()
            result = activate.entity_manager(entity_type=EntityManagerTypes.TAGS)
            MockTags.assert_called_once_with(mock_commcell)
            assert result is not None

    def test_entity_manager_classifiers_type(self, mock_commcell):
        activate = Activate(mock_commcell)
        with patch("cvpysdk.activate.Classifiers") as MockClassifiers:
            MockClassifiers.return_value = MagicMock()
            result = activate.entity_manager(entity_type=EntityManagerTypes.CLASSIFIERS)
            MockClassifiers.assert_called_once_with(mock_commcell)
            assert result is not None


@pytest.mark.unit
class TestActivateFSO:
    """Tests for Activate.file_storage_optimization."""

    def test_fso_servers_default(self, mock_commcell):
        activate = Activate(mock_commcell)
        with patch("cvpysdk.activate.FsoServers") as MockFso:
            MockFso.return_value = MagicMock()
            result = activate.file_storage_optimization()
            MockFso.assert_called_once_with(mock_commcell)
            assert result is not None

    def test_fso_server_groups(self, mock_commcell):
        activate = Activate(mock_commcell)
        with patch("cvpysdk.activate.FsoServerGroups") as MockFsoGroups:
            MockFsoGroups.return_value = MagicMock()
            result = activate.file_storage_optimization(fso_type=FsoTypes.SERVER_GROUPS)
            MockFsoGroups.assert_called_once_with(mock_commcell)
            assert result is not None

    def test_fso_bad_type_raises(self, mock_commcell):
        activate = Activate(mock_commcell)
        with pytest.raises(SDKException):
            activate.file_storage_optimization(fso_type="invalid")


@pytest.mark.unit
class TestActivateSDG:
    """Tests for Activate.sensitive_data_governance."""

    def test_sdg_lazy_init(self, mock_commcell):
        activate = Activate(mock_commcell)
        with patch("cvpysdk.activate.Projects") as MockProjects:
            MockProjects.return_value = MagicMock()
            result = activate.sensitive_data_governance()
            MockProjects.assert_called_once_with(mock_commcell)
            assert result is not None

    def test_sdg_cached(self, mock_commcell):
        activate = Activate(mock_commcell)
        with patch("cvpysdk.activate.Projects") as MockProjects:
            mock_instance = MagicMock()
            MockProjects.return_value = mock_instance
            result1 = activate.sensitive_data_governance()
            result2 = activate.sensitive_data_governance()
            MockProjects.assert_called_once()
            assert result1 is result2
