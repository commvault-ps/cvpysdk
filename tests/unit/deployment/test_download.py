"""Unit tests for cvpysdk.deployment.download module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.deployment.download import Download
from cvpysdk.exception import SDKException


@pytest.mark.unit
class TestDownload:
    """Tests for the Download class."""

    def _create_download(self, mock_commcell, version=35):
        mock_commcell.commserv_version = version
        mock_commcell.version = "11.32"
        dl = Download(mock_commcell)
        return dl

    def test_init(self, mock_commcell):
        dl = self._create_download(mock_commcell)
        assert dl.commcell_object is mock_commcell
        assert dl.update_option == {}

    @patch("cvpysdk.deployment.download.Job")
    def test_download_software_default_options(self, mock_job, mock_commcell, mock_response):
        dl = self._create_download(mock_commcell, version=35)
        resp = mock_response(json_data={"jobIds": [123]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = dl.download_software()
        assert result is not None
        mock_job.assert_called_once()

    @patch("cvpysdk.deployment.download.Job")
    def test_download_software_latest_sp_v36(self, mock_job, mock_commcell, mock_response):
        dl = self._create_download(mock_commcell, version=36)
        resp = mock_response(json_data={"jobId": 456})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = dl.download_software(options="latest service pack")
        assert result is not None

    def test_download_software_sp_and_hotfix_no_sp(self, mock_commcell, mock_response):
        dl = self._create_download(mock_commcell)
        with pytest.raises(SDKException):
            dl.download_software(options="service pack and hotfixes", service_pack=None)

    @patch("cvpysdk.deployment.download.Job")
    def test_download_software_sp_and_hotfix_with_sp(self, mock_job, mock_commcell, mock_response):
        dl = self._create_download(mock_commcell, version=35)
        resp = mock_response(json_data={"jobIds": [789]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = dl.download_software(
            options="service pack and hotfixes",
            service_pack=13,
            cu_number=5,
        )
        assert result is not None

    @patch("cvpysdk.deployment.download.Job")
    def test_sync_remote_cache_default(self, mock_job, mock_commcell, mock_response):
        dl = self._create_download(mock_commcell)
        resp = mock_response(json_data={"jobIds": [111]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = dl.sync_remote_cache()
        assert result is not None

    @patch("cvpysdk.deployment.download.Job")
    def test_sync_remote_cache_with_clients(self, mock_job, mock_commcell, mock_response):
        dl = self._create_download(mock_commcell)
        resp = mock_response(json_data={"jobIds": [222]})
        mock_commcell._cvpysdk_object.make_request.return_value = (True, resp)
        mock_job.return_value = MagicMock()
        result = dl.sync_remote_cache(client_list=["client1", "client2"])
        assert result is not None
