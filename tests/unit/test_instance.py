"""Unit tests for cvpysdk/instance.py module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.instance import Instances


def _make_agent_object(mock_commcell):
    """Helper to build an agent-like mock."""
    client = MagicMock()
    client._commcell_object = mock_commcell
    client.client_id = "1"
    client.client_name = "testclient"

    agent = MagicMock()
    agent._client_object = client
    agent._commcell_object = mock_commcell
    agent.agent_name = "file system"
    agent.agent_id = "33"
    return agent


@pytest.mark.unit
class TestInstancesInit:
    """Tests for the Instances collection class."""

    def test_repr(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        with patch.object(Instances, "_get_instances", return_value={}):
            instances = Instances(agent)
        assert "Instances" in repr(instances)
        assert "file system" in repr(instances)

    def test_all_instances_property(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        data = {"defaultinstancename": "1"}
        with patch.object(Instances, "_get_instances", return_value=data):
            instances = Instances(agent)
        assert instances.all_instances == data

    def test_len(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        data = {"instance1": "1", "instance2": "2"}
        with patch.object(Instances, "_get_instances", return_value=data):
            instances = Instances(agent)
        assert len(instances) == 2


@pytest.mark.unit
class TestInstancesHasInstance:
    """Tests for Instances.has_instance."""

    def test_has_instance_true(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        data = {"defaultinstancename": "1"}
        with patch.object(Instances, "_get_instances", return_value=data):
            instances = Instances(agent)
        assert instances.has_instance("defaultinstancename") is True

    def test_has_instance_bad_type_raises(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        with patch.object(Instances, "_get_instances", return_value={}):
            instances = Instances(agent)
        with pytest.raises(SDKException):
            instances.has_instance(123)


@pytest.mark.unit
class TestInstancesGetItem:
    """Tests for Instances.__getitem__."""

    def test_getitem_by_name(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        data = {"myinstance": "42"}
        with patch.object(Instances, "_get_instances", return_value=data):
            instances = Instances(agent)
        assert instances["myinstance"] == "42"

    def test_getitem_by_id(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        data = {"myinstance": "42"}
        with patch.object(Instances, "_get_instances", return_value=data):
            instances = Instances(agent)
        assert instances["42"] == "myinstance"

    def test_getitem_not_found(self, mock_commcell):
        agent = _make_agent_object(mock_commcell)
        with patch.object(Instances, "_get_instances", return_value={}):
            instances = Instances(agent)
        with pytest.raises(IndexError):
            instances["nonexistent"]
