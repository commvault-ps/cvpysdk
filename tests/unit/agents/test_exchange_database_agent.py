"""Unit tests for cvpysdk.agents.exchange_database_agent module."""

from unittest.mock import MagicMock, patch

import pytest

from cvpysdk.agents.exchange_database_agent import ExchangeDatabaseAgent


@pytest.mark.unit
class TestExchangeDatabaseAgent:
    """Tests for the ExchangeDatabaseAgent class."""

    def _make_agent(self):
        """Create an ExchangeDatabaseAgent with mocked internals."""
        agent = object.__new__(ExchangeDatabaseAgent)
        agent._subclients = None
        agent._instance_object = MagicMock()
        agent._backupset_object = MagicMock()
        return agent

    def test_subclients_property(self):
        """Test subclients property returns Subclients instance."""
        agent = self._make_agent()
        agent._commcell_object = MagicMock()

        with patch("cvpysdk.agents.exchange_database_agent.Subclients") as mock_subclients_cls:
            mock_subclients_cls.return_value = MagicMock()
            _ = agent.subclients
            mock_subclients_cls.assert_called_once_with(agent)

    def test_subclients_property_cached(self):
        """Test subclients property returns cached value on second call."""
        agent = self._make_agent()
        cached = MagicMock()
        agent._subclients = cached
        assert agent.subclients is cached

    def test_backup_delegates_to_backupset(self):
        """Test backup method delegates to backupset."""
        agent = self._make_agent()
        agent._backupset_object.backup.return_value = ["job1"]
        assert agent.backup() == ["job1"]
        agent._backupset_object.backup.assert_called_once()

    def test_browse_delegates_to_instance(self):
        """Test browse method delegates to instance."""
        agent = self._make_agent()
        agent._instance_object.browse.return_value = (["path1"], {"path1": {}})
        agent.browse(path="c:\\test")
        agent._instance_object.browse.assert_called_once_with(path="c:\\test")

    def test_find_delegates_to_instance(self):
        """Test find method delegates to instance."""
        agent = self._make_agent()
        agent._instance_object.find.return_value = (["path1"], {"path1": {}})
        agent.find(file_name="*.txt")
        agent._instance_object.find.assert_called_once_with(file_name="*.txt")

    @patch("cvpysdk.agents.exchange_database_agent.Agent.refresh", return_value=None)
    def test_refresh_resets_subclients(self, mock_refresh):
        """Test refresh clears subclients cache."""
        agent = self._make_agent()
        agent._subclients = MagicMock()
        agent.refresh()
        assert agent._subclients is None
