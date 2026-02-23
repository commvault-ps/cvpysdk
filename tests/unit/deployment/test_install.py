"""Unit tests for cvpysdk.deployment.install module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.deployment.install import Install
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestInstall:
    """Tests for the Install class."""

    def _create_install(self, mock_commcell, version=35):
        mock_commcell.commserv_version = version
        mock_commcell.clients.all_clients = {
            "client1": {"id": "1"},
            "client2": {"id": "2"},
        }
        mock_commcell.client_groups.all_clientgroups = {"group1": "10"}
        inst = Install(mock_commcell)
        return inst

    def test_init(self, mock_commcell):
        inst = self._create_install(mock_commcell)
        assert inst.commcell_object is mock_commcell

    def test_repair_software_invalid_client(self, mock_commcell):
        inst = self._create_install(mock_commcell)
        with pytest.raises(SDKException):
            inst.repair_software(client="nonexistent_client")

    def test_repair_software_invalid_client_group(self, mock_commcell):
        inst = self._create_install(mock_commcell)
        with pytest.raises(SDKException):
            inst.repair_software(client_group="nonexistent_group")

    @patch("cvpysdk.deployment.install.Job")
    def test_repair_software_success(self, mock_job, mock_commcell, mock_response):
        inst = self._create_install(mock_commcell)
        resp = mock_response(json_data={"jobIds": [100]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = inst.repair_software(client="client1")
        assert result is not None

    @patch("cvpysdk.deployment.install.Job")
    def test_repair_software_with_group(self, mock_job, mock_commcell, mock_response):
        inst = self._create_install(mock_commcell)
        resp = mock_response(json_data={"jobIds": [101]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = inst.repair_software(client_group="group1")
        assert result is not None

    def test_repair_software_api_failure(self, mock_commcell, mock_response):
        inst = self._create_install(mock_commcell)
        resp = mock_response(status_code=500, text="error")
        mock_commcell._cvpysdk_object.make_request.return_value = (False, resp)
        with pytest.raises(SDKException):
            inst.repair_software(client="client1")

    def test_push_servicepack_no_targets(self, mock_commcell):
        inst = self._create_install(mock_commcell)
        with pytest.raises(SDKException):
            inst.push_servicepack_and_hotfix()

    def test_push_servicepack_invalid_clients(self, mock_commcell):
        inst = self._create_install(mock_commcell)
        with pytest.raises(SDKException):
            inst.push_servicepack_and_hotfix(client_computers=["nonexistent"])

    def test_push_servicepack_invalid_groups(self, mock_commcell):
        inst = self._create_install(mock_commcell)
        with pytest.raises(SDKException):
            inst.push_servicepack_and_hotfix(client_computer_groups=["nonexistent"])

    @patch("cvpysdk.deployment.install.Job")
    def test_push_servicepack_success(self, mock_job, mock_commcell, mock_response):
        inst = self._create_install(mock_commcell)
        resp = mock_response(json_data={"jobIds": [200]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = inst.push_servicepack_and_hotfix(client_computers=["client1"])
        assert result is not None

    @patch("cvpysdk.deployment.install.Job")
    def test_push_servicepack_v36(self, mock_job, mock_commcell, mock_response):
        inst = self._create_install(mock_commcell, version=36)
        resp = mock_response(json_data={"jobId": 300})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = inst.push_servicepack_and_hotfix(client_computers=["client1"])
        assert result is not None

    def test_install_software_no_features(self, mock_commcell):
        inst = self._create_install(mock_commcell)
        with pytest.raises(SDKException):
            inst.install_software(client_computers=["host1"])

    def test_install_software_no_clients(self, mock_commcell):
        inst = self._create_install(mock_commcell)
        with pytest.raises(SDKException):
            inst.install_software(windows_features=[702])

    @patch("cvpysdk.deployment.install.Job")
    def test_install_software_windows_success(self, mock_job, mock_commcell, mock_response):
        inst = self._create_install(mock_commcell)
        resp = mock_response(json_data={"jobIds": [400]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = inst.install_software(
            client_computers=["host1"],
            windows_features=[702],
            username="admin",
            password="pass",
        )
        assert result is not None

    @patch("cvpysdk.deployment.install.Job")
    def test_install_software_unix_success(self, mock_job, mock_commcell, mock_response):
        inst = self._create_install(mock_commcell)
        resp = mock_response(json_data={"jobIds": [500]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = inst.install_software(
            client_computers=["linuxhost"],
            unix_features=[1101],
            username="root",
            password="pass",
        )
        assert result is not None
