"""Unit tests for cvpysdk/agent.py module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.agent import Agents
from cvpysdk.exception import SDKException


def _make_client_object(mock_commcell):
    """Helper to build a client-like mock."""
    client = MagicMock()
    client._commcell_object = mock_commcell
    client.client_id = "1"
    client.client_name = "testclient"
    client.vm_guid = None
    client.properties = {}
    return client


@pytest.mark.unit
class TestAgentsInit:
    """Tests for the Agents collection class."""

    def test_repr(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        with patch.object(Agents, "_get_agents", return_value={}):
            agents = Agents(client)
        assert "Agents" in repr(agents)
        assert "testclient" in repr(agents)

    def test_all_agents_property(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        data = {"file system": "33"}
        with patch.object(Agents, "_get_agents", return_value=data):
            agents = Agents(client)
        assert agents.all_agents == data

    def test_len(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        data = {"file system": "33", "virtual server": "106"}
        with patch.object(Agents, "_get_agents", return_value=data):
            agents = Agents(client)
        assert len(agents) == 2


@pytest.mark.unit
class TestAgentsHasAgent:
    """Tests for Agents.has_agent."""

    def test_has_agent_true(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        data = {"file system": "33"}
        with patch.object(Agents, "_get_agents", return_value=data):
            agents = Agents(client)
        assert agents.has_agent("file system") is True

    def test_has_agent_bad_type_raises(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        with patch.object(Agents, "_get_agents", return_value={}):
            agents = Agents(client)
        with pytest.raises(SDKException):
            agents.has_agent(123)

    def test_has_agent_case_insensitive(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        data = {"file system": "33"}
        with patch.object(Agents, "_get_agents", return_value=data):
            agents = Agents(client)
        assert agents.has_agent("File System") is True


@pytest.mark.unit
class TestAgentsGetItem:
    """Tests for Agents.__getitem__."""

    def test_getitem_by_name(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        data = {"file system": "33"}
        with patch.object(Agents, "_get_agents", return_value=data):
            agents = Agents(client)
        assert agents["file system"] == "33"

    def test_getitem_by_id(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        data = {"file system": "33"}
        with patch.object(Agents, "_get_agents", return_value=data):
            agents = Agents(client)
        assert agents["33"] == "file system"

    def test_getitem_not_found(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        with patch.object(Agents, "_get_agents", return_value={}):
            agents = Agents(client)
        with pytest.raises(IndexError):
            agents["nonexistent"]


@pytest.mark.unit
class TestAgentsGet:
    """Tests for Agents.get method."""

    def test_get_nonexistent_raises(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        with patch.object(Agents, "_get_agents", return_value={}):
            agents = Agents(client)
        with pytest.raises(SDKException):
            agents.get("nonexistent")

    def test_get_bad_type_raises(self, mock_commcell):
        client = _make_client_object(mock_commcell)
        with patch.object(Agents, "_get_agents", return_value={}):
            agents = Agents(client)
        with pytest.raises(SDKException):
            agents.get(123)
