"""Tests for cvpysdk/backupsets/vsbackupset.py (VSBackupset)."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.backupset import Backupset
from cvpysdk.backupsets.vsbackupset import VSBackupset
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestVSBackupsetInheritance:
    def test_inherits_backupset(self):
        assert issubclass(VSBackupset, Backupset)

    def test_has_browse_method(self):
        assert hasattr(VSBackupset, "browse")

    def test_has_process_browse_response(self):
        assert hasattr(VSBackupset, "_process_browse_response")

    def test_has_hidden_subclient_property(self):
        assert isinstance(VSBackupset.__dict__.get("hidden_subclient"), property)

    def test_has_index_server_property(self):
        assert isinstance(VSBackupset.__dict__.get("index_server"), property)

    def test_has_vm_filter_property(self):
        assert isinstance(VSBackupset.__dict__.get("vm_filter"), property)

    def test_has_vm_disk_filter_property(self):
        assert isinstance(VSBackupset.__dict__.get("vm_disk_filter"), property)


@pytest.mark.unit
class TestVSBackupsetNew:
    def test_new_returns_base_class_for_unknown_instance(self):
        instance_object = MagicMock()
        instance_object.instance_name = "nonexistent_instance_xyz"
        result = VSBackupset.__new__(VSBackupset, instance_object, "test_bs")
        assert type(result) is VSBackupset

    def test_new_returns_vmware_for_vmware_instance(self):
        from cvpysdk.backupsets._virtual_server.vmware import VMwareBackupset

        instance_object = MagicMock()
        instance_object.instance_name = "vmware"
        result = VSBackupset.__new__(VSBackupset, instance_object, "test_bs")
        assert isinstance(result, VMwareBackupset)

    def test_new_returns_kubernetes_for_kubernetes_instance(self):
        from cvpysdk.backupsets._virtual_server.kubernetes import (
            KubernetesBackupset,
        )

        instance_object = MagicMock()
        instance_object.instance_name = "kubernetes"
        result = VSBackupset.__new__(VSBackupset, instance_object, "test_bs")
        assert isinstance(result, KubernetesBackupset)

    def test_new_strips_special_chars_from_instance_name(self):
        instance_object = MagicMock()
        instance_object.instance_name = "non-existent!@#"
        # Should not raise; falls back to base class
        result = VSBackupset.__new__(VSBackupset, instance_object, "test_bs")
        assert type(result) is VSBackupset


@pytest.mark.unit
class TestVSBackupsetBrowse:
    def _make_instance(self):
        inst = object.__new__(VSBackupset)
        inst._do_browse = MagicMock(return_value=(["path1"], {"path1": {}}))
        return inst

    def test_browse_with_kwargs(self):
        inst = self._make_instance()
        inst.browse(path="c:\\test")
        inst._do_browse.assert_called_once()
        opts = inst._do_browse.call_args[0][0]
        assert opts["retry_count"] == 0
        assert opts["path"] == "c:\\test"

    def test_browse_with_dict_arg(self):
        inst = self._make_instance()
        inst.browse({"path": "\\vm", "show_deleted": True})
        opts = inst._do_browse.call_args[0][0]
        assert opts["retry_count"] == 0
        assert opts["show_deleted"] is True


@pytest.mark.unit
class TestVSBackupsetProcessBrowseResponse:
    def _make_instance(self):
        inst = object.__new__(VSBackupset)
        inst._update_response_ = MagicMock(return_value="error text")
        return inst

    def test_raises_on_flag_false(self):
        inst = self._make_instance()
        response = MagicMock()
        response.text = "error"
        with pytest.raises(SDKException):
            inst._process_browse_response(False, response, {"retry_count": 0})

    def test_returns_empty_for_live_browse_message(self):
        inst = self._make_instance()
        response = MagicMock()
        response.json.return_value = {
            "browseResponses": [
                {
                    "respType": 0,
                    "messages": [
                        {
                            "errorMessage": (
                                "Please note that this is a live browse operation. "
                                "Live browse operations can take some time before "
                                "the results appear in the browse window."
                            )
                        }
                    ],
                }
            ]
        }
        paths, paths_dict = inst._process_browse_response(
            True, response, {"retry_count": 0, "show_deleted": False}
        )
        assert paths == []
        assert paths_dict == {}

    def test_processes_valid_result_set(self):
        inst = self._make_instance()
        response = MagicMock()
        response.json.return_value = {
            "browseResponses": [
                {
                    "respType": 0,
                    "browseResult": {
                        "dataResultSet": [
                            {
                                "displayName": "VM1",
                                "name": "snap_vm1",
                                "path": "\\VM1",
                                "modificationTime": "0",
                                "size": "1024",
                                "flags": {"file": False},
                                "advancedData": {"backupTime": "0"},
                            }
                        ]
                    },
                }
            ]
        }
        paths, paths_dict = inst._process_browse_response(
            True,
            response,
            {
                "retry_count": 0,
                "show_deleted": False,
                "operation": "browse",
                "path": "\\",
            },
        )
        assert "\\VM1" in paths
        assert paths_dict["\\VM1"]["name"] == "VM1"
        assert paths_dict["\\VM1"]["type"] == "Folder"


@pytest.mark.unit
class TestVSBackupsetIndexServer:
    def _make_instance(self):
        inst = object.__new__(VSBackupset)
        inst._commcell_object = MagicMock()
        inst._process_update_reponse = MagicMock()
        return inst

    def test_index_server_returns_none_when_no_settings(self):
        inst = self._make_instance()
        inst._properties = {}
        assert inst.index_server is None

    @patch("cvpysdk.backupsets.vsbackupset.Client")
    def test_index_server_returns_client(self, mock_client_cls):
        inst = self._make_instance()
        inst._properties = {"indexSettings": {"currentIndexServer": {"clientName": "idx_server"}}}
        mock_client_cls.return_value = MagicMock()
        result = inst.index_server
        mock_client_cls.assert_called_once_with(inst._commcell_object, client_name="idx_server")
        assert result is not None

    def test_index_server_setter_raises_for_non_client(self):
        inst = self._make_instance()
        inst._properties = {}
        with pytest.raises(SDKException):
            inst.index_server = "not_a_client_object"
