"""Unit tests for cvpysdk/backupset.py module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.backupset import Backupsets
from cvpysdk.exception import SDKException


def _make_agent_object(mock_commcell):
    """Helper to build an agent-like mock for Backupsets."""
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
    return agent


@pytest.mark.unit
class TestBackupsetsInit:
    """Tests for the Backupsets collection class."""

    def test_repr(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        with patch.object(Backupsets, "_get_backupsets", return_value={}):
            backupsets = Backupsets(agent)
        assert "Backupsets" in repr(backupsets)

    def test_invalid_class_object_raises(self, mock_commcell):
        with pytest.raises(SDKException):
            Backupsets("not_an_agent_or_instance")

    def test_all_backupsets_property(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        data = {"defaultbackupset": "1"}
        with patch.object(Backupsets, "_get_backupsets", return_value=data):
            backupsets = Backupsets(agent)
        assert backupsets.all_backupsets == data


@pytest.mark.unit
class TestBackupsetsHasBackupset:
    """Tests for Backupsets.has_backupset."""

    def test_has_backupset_true(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        data = {"defaultbackupset": "1"}
        with patch.object(Backupsets, "_get_backupsets", return_value=data):
            backupsets = Backupsets(agent)
        assert backupsets.has_backupset("defaultbackupset") is True

    def test_has_backupset_bad_type_raises(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        with patch.object(Backupsets, "_get_backupsets", return_value={}):
            backupsets = Backupsets(agent)
        with pytest.raises(SDKException):
            backupsets.has_backupset(123)


@pytest.mark.unit
class TestBackupsetsGetItem:
    """Tests for Backupsets.__getitem__."""

    def test_getitem_by_name(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        data = {"defaultbackupset": "1"}
        with patch.object(Backupsets, "_get_backupsets", return_value=data):
            backupsets = Backupsets(agent)
        assert backupsets["defaultbackupset"] == "1"

    def test_getitem_not_found(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        with patch.object(Backupsets, "_get_backupsets", return_value={}):
            backupsets = Backupsets(agent)
        with pytest.raises(IndexError):
            backupsets["nonexistent"]
