"""Unit tests for cvpysdk/subclient.py module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.subclient import Subclient, Subclients


def _make_agent_object(mock_commcell):
    """Helper to build an agent-like mock for Subclients."""
    from cvpysdk.agent import Agent

    client = MagicMock()
    client._commcell_object = mock_commcell
    client.client_id = "1"
    client.client_name = "testclient"

    agent = MagicMock(spec=Agent)
    agent._client_object = client
    agent._commcell_object = mock_commcell
    agent.agent_name = "file system"
    agent.agent_id = "33"
    agent.instances = MagicMock()
    agent.instances.all_instances = {"default": "1"}
    return agent


def _make_backupset_object(mock_commcell):
    """Helper to build a backupset-like mock for Subclients."""
    from cvpysdk.backupset import Backupset

    client = MagicMock()
    client._commcell_object = mock_commcell
    client.client_id = "1"
    client.client_name = "testclient"

    agent = MagicMock()
    agent._client_object = client
    agent._commcell_object = mock_commcell
    agent.agent_name = "file system"
    agent.agent_id = "33"

    instance = MagicMock()
    instance._agent_object = agent
    instance.instance_name = "default"
    instance.instance_id = "1"
    instance.backupsets = MagicMock()
    instance.backupsets.all_backupsets = {"defaultbackupset": "1"}

    bs = MagicMock(spec=Backupset)
    bs._instance_object = instance
    bs._agent_object = agent
    bs._client_object = client
    bs.backupset_name = "defaultbackupset"
    bs.backupset_id = "1"
    return bs


@pytest.mark.unit
class TestSubclientsInit:
    """Tests for the Subclients collection class."""

    def test_repr_with_backupset(self, mock_commcell):
        bs = _make_backupset_object(mock_commcell)
        with patch.object(Subclients, "_get_subclients", return_value={}):
            subclients = Subclients(bs)
        result = repr(subclients)
        assert "Subclients" in result

    def test_invalid_class_object_raises(self, mock_commcell):
        with pytest.raises(SDKException):
            Subclients("not_valid_class")


@pytest.mark.unit
class TestSubclientsHasSubclient:
    """Tests for Subclients.has_subclient."""

    def test_has_subclient_true(self, mock_commcell):
        bs = _make_backupset_object(mock_commcell)
        data = {"default": {"id": "1", "backupset": "defaultbackupset"}}
        with patch.object(Subclients, "_get_subclients", return_value=data):
            subclients = Subclients(bs)
        assert subclients.has_subclient("default") is True

    def test_has_subclient_false(self, mock_commcell):
        bs = _make_backupset_object(mock_commcell)
        with patch.object(Subclients, "_get_subclients", return_value={}):
            subclients = Subclients(bs)
        assert not subclients.has_subclient("nonexistent")

    def test_has_subclient_bad_type_raises(self, mock_commcell):
        bs = _make_backupset_object(mock_commcell)
        with patch.object(Subclients, "_get_subclients", return_value={}):
            subclients = Subclients(bs)
        with pytest.raises(SDKException):
            subclients.has_subclient(123)


@pytest.mark.unit
class TestSubclientsGetItem:
    """Tests for Subclients.__getitem__."""

    def test_getitem_by_name(self, mock_commcell):
        bs = _make_backupset_object(mock_commcell)
        data = {"default": {"id": "1", "backupset": "defaultbackupset"}}
        with patch.object(Subclients, "_get_subclients", return_value=data):
            subclients = Subclients(bs)
        result = subclients["default"]
        assert result["id"] == "1"

    def test_getitem_by_id(self, mock_commcell):
        bs = _make_backupset_object(mock_commcell)
        data = {"default": {"id": "1", "backupset": "defaultbackupset"}}
        with patch.object(Subclients, "_get_subclients", return_value=data):
            subclients = Subclients(bs)
        result = subclients["1"]
        assert result == "default"

    def test_getitem_not_found(self, mock_commcell):
        bs = _make_backupset_object(mock_commcell)
        with patch.object(Subclients, "_get_subclients", return_value={}):
            subclients = Subclients(bs)
        with pytest.raises(IndexError):
            subclients["nonexistent"]


@pytest.mark.unit
class TestSubclientsLen:
    """Tests for Subclients.__len__."""

    def test_len(self, mock_commcell):
        bs = _make_backupset_object(mock_commcell)
        data = {
            "sc1": {"id": "1", "backupset": "bs"},
            "sc2": {"id": "2", "backupset": "bs"},
        }
        with patch.object(Subclients, "_get_subclients", return_value=data):
            subclients = Subclients(bs)
        assert len(subclients) == 2


@pytest.mark.unit
class TestSubclientRepr:
    """Tests for Subclient __repr__."""

    def test_repr(self):
        sc = object.__new__(Subclient)
        sc._subclient_name = "default"
        sc._backupset_object = MagicMock()
        sc._backupset_object.backupset_name = "defaultbackupset"
        result = repr(sc)
        assert "default" in result
