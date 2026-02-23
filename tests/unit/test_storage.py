from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.storage import DiskLibraries, Libraries, MediaAgent, MediaAgents


@pytest.mark.unit
class TestMediaAgents:
    """Tests for the MediaAgents collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(MediaAgents, "_get_media_agents", return_value={}):
            ma = MediaAgents(mock_commcell)
        assert "MediaAgents" in repr(ma)

    def test_all_media_agents_property(self, mock_commcell):
        agents = {"ma1": {"id": "1", "os_info": "Windows", "is_online": True}}
        with patch.object(MediaAgents, "_get_media_agents", return_value=agents):
            ma = MediaAgents(mock_commcell)
        assert ma.all_media_agents == agents

    def test_has_media_agent_true(self, mock_commcell):
        agents = {"ma1": {"id": "1", "os_info": "Windows", "is_online": True}}
        with patch.object(MediaAgents, "_get_media_agents", return_value=agents):
            ma = MediaAgents(mock_commcell)
        assert ma.has_media_agent("ma1") is True

    def test_has_media_agent_false(self, mock_commcell):
        agents = {"ma1": {"id": "1", "os_info": "Windows", "is_online": True}}
        with patch.object(MediaAgents, "_get_media_agents", return_value=agents):
            ma = MediaAgents(mock_commcell)
        assert ma.has_media_agent("nonexistent") is False

    def test_has_media_agent_case_insensitive(self, mock_commcell):
        agents = {"ma1": {"id": "1", "os_info": "Windows", "is_online": True}}
        with patch.object(MediaAgents, "_get_media_agents", return_value=agents):
            ma = MediaAgents(mock_commcell)
        assert ma.has_media_agent("MA1") is True

    def test_has_media_agent_bad_type_raises(self, mock_commcell):
        with patch.object(MediaAgents, "_get_media_agents", return_value={}):
            ma = MediaAgents(mock_commcell)
        with pytest.raises(SDKException):
            ma.has_media_agent(123)

    def test_get_returns_media_agent(self, mock_commcell):
        agents = {"ma1": {"id": "1", "os_info": "Windows", "is_online": True}}
        with patch.object(MediaAgents, "_get_media_agents", return_value=agents):
            ma = MediaAgents(mock_commcell)
        with patch.object(MediaAgent, "__init__", return_value=None):
            result = ma.get("ma1")
        assert isinstance(result, MediaAgent)

    def test_get_nonexistent_raises(self, mock_commcell):
        with patch.object(MediaAgents, "_get_media_agents", return_value={}):
            ma = MediaAgents(mock_commcell)
        with pytest.raises(SDKException):
            ma.get("nonexistent")

    def test_get_bad_type_raises(self, mock_commcell):
        with patch.object(MediaAgents, "_get_media_agents", return_value={}):
            ma = MediaAgents(mock_commcell)
        with pytest.raises(SDKException):
            ma.get(123)

    def test_delete_bad_type_raises(self, mock_commcell):
        with patch.object(MediaAgents, "_get_media_agents", return_value={}):
            ma = MediaAgents(mock_commcell)
        with pytest.raises(SDKException):
            ma.delete(123)

    def test_delete_nonexistent_raises(self, mock_commcell):
        with patch.object(MediaAgents, "_get_media_agents", return_value={}):
            ma = MediaAgents(mock_commcell)
        with pytest.raises(SDKException):
            ma.delete("nonexistent")

    def test_str_representation(self, mock_commcell):
        agents = {"ma1": {"id": "1", "os_info": "Windows", "is_online": True}}
        with patch.object(MediaAgents, "_get_media_agents", return_value=agents):
            ma = MediaAgents(mock_commcell)
        result = str(ma)
        assert "ma1" in result

    def test_refresh(self, mock_commcell):
        with patch.object(MediaAgents, "_get_media_agents", return_value={}) as mock_get:
            ma = MediaAgents(mock_commcell)
            ma.refresh()
        assert mock_get.call_count == 2


@pytest.mark.unit
class TestMediaAgent:
    """Tests for the MediaAgent entity class."""

    def test_repr(self, mock_commcell):
        with patch.object(MediaAgent, "_initialize_media_agent_properties"):
            ma = MediaAgent(mock_commcell, "ma1", "1")
        assert "ma1" in repr(ma)
        assert "testcs" in repr(ma)

    def test_media_agent_name_property(self, mock_commcell):
        with patch.object(MediaAgent, "_initialize_media_agent_properties"):
            ma = MediaAgent(mock_commcell, "MA1", "1")
        assert ma.media_agent_name == "ma1"

    def test_media_agent_id_property(self, mock_commcell):
        with patch.object(MediaAgent, "_initialize_media_agent_properties"):
            ma = MediaAgent(mock_commcell, "ma1", "123")
        assert ma.media_agent_id == "123"


@pytest.mark.unit
class TestDiskLibraries:
    """Tests for the DiskLibraries collection class."""

    def test_repr(self, mock_commcell):
        with patch.object(Libraries, "_get_libraries", return_value={}):
            dl = DiskLibraries(mock_commcell)
        assert "DiskLibraries" in repr(dl)

    def test_all_disk_libraries_property(self, mock_commcell):
        libs = {"lib1": "1", "lib2": "2"}
        with patch.object(Libraries, "_get_libraries", return_value=libs):
            dl = DiskLibraries(mock_commcell)
        assert dl.all_disk_libraries == libs

    def test_has_library_true(self, mock_commcell):
        libs = {"lib1": "1"}
        with patch.object(Libraries, "_get_libraries", return_value=libs):
            dl = DiskLibraries(mock_commcell)
        assert dl.has_library("lib1") is True

    def test_has_library_false(self, mock_commcell):
        libs = {"lib1": "1"}
        with patch.object(Libraries, "_get_libraries", return_value=libs):
            dl = DiskLibraries(mock_commcell)
        assert dl.has_library("nonexistent") is False

    def test_has_library_bad_type_raises(self, mock_commcell):
        with patch.object(Libraries, "_get_libraries", return_value={}):
            dl = DiskLibraries(mock_commcell)
        with pytest.raises(SDKException):
            dl.has_library(123)

    def test_str_representation(self, mock_commcell):
        libs = {"lib1": "1"}
        with patch.object(Libraries, "_get_libraries", return_value=libs):
            dl = DiskLibraries(mock_commcell)
        result = str(dl)
        assert "lib1" in result
