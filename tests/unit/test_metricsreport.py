from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.metricsreport import _Metrics

SAMPLE_METRICS_CONFIG = {
    "config": {
        "cloud": {
            "serviceList": [
                {"service": {"name": "Health Check"}, "enabled": True},
                {"service": {"name": "Activity"}, "enabled": False},
                {"service": {"name": "Audit"}, "enabled": False},
                {"service": {"name": "Post Upgrade Check"}, "enabled": False},
                {"service": {"name": "Charge Back"}, "enabled": False},
            ]
        },
        "scriptDownloadTime": 1000000,
        "lastCollectionTime": 2000000,
        "lastUploadTime": 3000000,
        "nextUploadTime": 4000000,
        "uploadFrequency": 1,
    }
}


def _mock_get_metrics_config(self):
    """Mock the _get_metrics_config method to set up config data."""
    self._metrics_config = SAMPLE_METRICS_CONFIG.copy()
    self._metrics_config.update({"isPrivateCloud": bool(self._isprivate == 1)})
    self._cloud = self._metrics_config["config"]["cloud"]
    self._service_list = self._cloud["serviceList"]
    self.services = {}
    for svc in self._service_list:
        self.services[svc["service"]["name"]] = svc["enabled"]


@pytest.mark.unit
class TestMetrics:
    """Tests for the _Metrics base class."""

    def test_repr_private(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        assert "Private" in repr(m)

    def test_repr_public(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 0)
        assert "Public" in repr(m)

    def test_enable_health(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        m.services["Health Check"] = False
        m.enable_health()
        assert m.services["Health Check"] is True

    def test_disable_health(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        m.disable_health()
        assert m.services["Health Check"] is False

    def test_enable_activity(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        m.enable_activity()
        assert m.services["Activity"] is True

    def test_disable_activity(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        m.services["Activity"] = True
        m.disable_activity()
        assert m.services["Activity"] is False

    def test_set_upload_freq_valid(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        m.set_upload_freq(3)
        assert m._metrics_config["config"]["uploadFrequency"] == 3

    def test_set_upload_freq_invalid_raises(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        with pytest.raises(SDKException):
            m.set_upload_freq(0)

    def test_set_data_collection_window_valid(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        m.set_data_collection_window(28800)
        assert m._metrics_config["config"]["dataCollectionTime"] == 28800

    def test_set_data_collection_window_invalid_raises(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        with pytest.raises(SDKException):
            m.set_data_collection_window(100)

    def test_remove_data_collection_window(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        m.remove_data_collection_window()
        assert m._metrics_config["config"]["dataCollectionTime"] == -1

    def test_lastdownloadtime_property(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        assert m.lastdownloadtime == 1000000

    def test_enable_all_services(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        m.enable_all_services()
        for name, enabled in m.services.items():
            if name not in ["Post Upgrade Check", "Upgrade Readiness"]:
                assert enabled is True

    def test_disable_all_services(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        m.enable_all_services()
        m.disable_all_services()
        for name, enabled in m.services.items():
            if name not in ["Post Upgrade Check", "Upgrade Readiness"]:
                assert enabled is False

    def test_set_all_clientgroups(self, mock_commcell):
        with patch.object(_Metrics, "_get_metrics_config", _mock_get_metrics_config):
            m = _Metrics(mock_commcell, 1)
        m.set_all_clientgroups()
        assert m._metrics_config["config"]["clientGroupList"] == [
            {"_type_": 28, "clientGroupId": -1}
        ]
