from unittest.mock import patch

import pytest

from cvpysdk.exception import SDKException
from cvpysdk.policies.configuration_policies import (
    ArchivePolicy,
    CleanupPolicy,
    ConfigurationPolicies,
    ConfigurationPolicy,
    ContentIndexingPolicy,
    JournalPolicy,
    RetentionPolicy,
)


@pytest.mark.unit
class TestConfigurationPolicies:
    """Tests for the ConfigurationPolicies collection class."""

    def _make_policies(self, mock_commcell, policies=None, ci_policies=None):
        with patch.object(
            ConfigurationPolicies, "_get_policies", return_value=policies or {}
        ), patch.object(ConfigurationPolicies, "_get_ci_policies", return_value=ci_policies or {}):
            return ConfigurationPolicies(mock_commcell)

    def test_repr(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        assert "ConfigurationPolicies" in repr(cp)

    def test_has_policy_true(self, mock_commcell):
        cp = self._make_policies(mock_commcell, policies={"testpol": ["1", "1"]})
        assert cp.has_policy("testpol") is True

    def test_has_policy_case_insensitive(self, mock_commcell):
        cp = self._make_policies(mock_commcell, policies={"testpol": ["1", "1"]})
        assert cp.has_policy("TestPol") is True

    def test_has_policy_non_string_raises(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            cp.has_policy(123)

    def test_has_policy_ci_policy(self, mock_commcell):
        cp = self._make_policies(mock_commcell, ci_policies={"cipol": ["2", "5"]})
        assert cp.has_policy("cipol") is True

    def test_get_nonexistent_raises(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            cp.get("nosuch", "Archive")

    def test_get_non_string_raises(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            cp.get(123, "Archive")

    def test_get_returns_policy_object(self, mock_commcell):
        cp = self._make_policies(mock_commcell, policies={"testpol": ["1", "1"]})
        with patch.object(ConfigurationPolicy, "__init__", return_value=None):
            result = cp.get("testpol", "Archive")
        assert isinstance(result, ConfigurationPolicy)

    def test_get_policy_object_archive(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        result = cp.get_policy_object("Archive", "test_archive")
        assert isinstance(result, ArchivePolicy)

    def test_get_policy_object_journal(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        result = cp.get_policy_object("Journal", "test_journal")
        assert isinstance(result, JournalPolicy)

    def test_get_policy_object_cleanup(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        result = cp.get_policy_object("Cleanup", "test_cleanup")
        assert isinstance(result, CleanupPolicy)

    def test_get_policy_object_retention(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        result = cp.get_policy_object("Retention", "test_retention")
        assert isinstance(result, RetentionPolicy)

    def test_get_policy_object_content_indexing(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        result = cp.get_policy_object("ContentIndexing", "test_ci")
        assert isinstance(result, ContentIndexingPolicy)

    def test_get_policy_object_unsupported_type_raises(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            cp.get_policy_object("InvalidType", "test")

    def test_delete_non_string_raises(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            cp.delete(123)

    def test_delete_nonexistent_raises(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            cp.delete("nonexistent")

    def test_run_content_indexing_nonexistent_raises(self, mock_commcell):
        cp = self._make_policies(mock_commcell)
        with pytest.raises(SDKException):
            cp.run_content_indexing("nonexistent_ci")

    def test_refresh_calls_get_methods(self, mock_commcell):
        with patch.object(
            ConfigurationPolicies, "_get_policies", return_value={}
        ) as mock_get, patch.object(
            ConfigurationPolicies, "_get_ci_policies", return_value={}
        ) as mock_get_ci:
            cp = ConfigurationPolicies(mock_commcell)
            cp.refresh()
        assert mock_get.call_count == 2
        assert mock_get_ci.call_count == 2


@pytest.mark.unit
class TestConfigurationPolicy:
    """Tests for the ConfigurationPolicy entity class."""

    def test_init_with_id(self, mock_commcell):
        policy = ConfigurationPolicy(mock_commcell, "test_policy", "42")
        assert policy.configuration_policy_id == "42"
        assert policy.configuration_policy_name == "test_policy"

    def test_init_without_id_calls_get(self, mock_commcell):
        with patch.object(ConfigurationPolicy, "_get_configuration_policy_id", return_value="99"):
            policy = ConfigurationPolicy(mock_commcell, "test_policy")
        assert policy.configuration_policy_id == "99"


@pytest.mark.unit
class TestArchivePolicy:
    """Tests for the ArchivePolicy class."""

    def test_init_defaults(self, mock_commcell):
        policy = ArchivePolicy(mock_commcell, "test_archive")
        assert policy.name == "test_archive"
        assert policy.email_policy_type == 1
        assert policy.archive_mailbox is False
        assert policy.primary_mailbox is True

    def test_name_setter(self, mock_commcell):
        policy = ArchivePolicy(mock_commcell, "test_archive")
        policy.name = "new_name"
        assert policy.name == "new_name"

    def test_initialize_policy_json_structure(self, mock_commcell):
        policy = ArchivePolicy(mock_commcell, "test_archive")
        result = policy._initialize_policy_json()
        assert "policy" in result
        assert result["policy"]["policyType"] == 1
        assert result["policy"]["policyEntity"]["policyName"] == "test_archive"
        assert "archivePolicy" in result["policy"]["detail"]["emailPolicy"]

    def test_property_setters(self, mock_commcell):
        policy = ArchivePolicy(mock_commcell, "test_archive")
        policy.archive_mailbox = True
        assert policy.archive_mailbox is True
        policy.include_messages_larger_than = 100
        assert policy.include_messages_larger_than == 100


@pytest.mark.unit
class TestJournalPolicy:
    """Tests for the JournalPolicy class."""

    def test_init_defaults(self, mock_commcell):
        policy = JournalPolicy(mock_commcell, "test_journal")
        assert policy.name == "test_journal"
        assert policy.email_policy_type == 4
        assert policy.delete_archived_messages is True

    def test_initialize_policy_json_structure(self, mock_commcell):
        policy = JournalPolicy(mock_commcell, "test_journal")
        result = policy._initialize_policy_json()
        assert result["policy"]["detail"]["emailPolicy"]["emailPolicyType"] == 4
        assert "journalPolicy" in result["policy"]["detail"]["emailPolicy"]


@pytest.mark.unit
class TestCleanupPolicy:
    """Tests for the CleanupPolicy class."""

    def test_init_defaults(self, mock_commcell):
        policy = CleanupPolicy(mock_commcell, "test_cleanup")
        assert policy.name == "test_cleanup"
        assert policy.email_policy_type == 2
        assert policy.create_stubs is True

    def test_initialize_policy_json_structure(self, mock_commcell):
        policy = CleanupPolicy(mock_commcell, "test_cleanup")
        result = policy._initialize_policy_json()
        assert result["policy"]["detail"]["emailPolicy"]["emailPolicyType"] == 2
        assert "cleanupPolicy" in result["policy"]["detail"]["emailPolicy"]


@pytest.mark.unit
class TestRetentionPolicy:
    """Tests for the RetentionPolicy class."""

    def test_init_defaults(self, mock_commcell):
        policy = RetentionPolicy(mock_commcell, "test_retention")
        assert policy.name == "test_retention"
        assert policy.email_policy_type == 3
        assert policy.days_for_media_pruning == -1

    def test_initialize_policy_json_structure(self, mock_commcell):
        policy = RetentionPolicy(mock_commcell, "test_retention")
        result = policy._initialize_policy_json()
        assert result["policy"]["detail"]["emailPolicy"]["emailPolicyType"] == 3
        assert "retentionPolicy" in result["policy"]["detail"]["emailPolicy"]


@pytest.mark.unit
class TestContentIndexingPolicy:
    """Tests for the ContentIndexingPolicy class."""

    def test_init_defaults(self, mock_commcell):
        policy = ContentIndexingPolicy(mock_commcell, "test_ci")
        assert policy.name == "test_ci"
        assert policy.min_doc_size == 0
        assert policy.max_doc_size == 50
        assert policy.index_server_name is None
        assert policy.data_access_node is None

    def test_exclude_paths_default(self, mock_commcell):
        policy = ContentIndexingPolicy(mock_commcell, "test_ci")
        assert isinstance(policy.exclude_paths, list)
        assert "C:\\Windows" in policy.exclude_paths

    def test_initialize_policy_json_raises_on_bad_types(self, mock_commcell):
        policy = ContentIndexingPolicy(mock_commcell, "test_ci")
        # index_server_name is None by default, not a string
        with pytest.raises(SDKException):
            policy._initialize_policy_json()

    def test_property_setters(self, mock_commcell):
        policy = ContentIndexingPolicy(mock_commcell, "test_ci")
        policy.min_doc_size = 10
        assert policy.min_doc_size == 10
        policy.max_doc_size = 100
        assert policy.max_doc_size == 100
        policy.index_server_name = "myserver"
        assert policy.index_server_name == "myserver"
        policy.data_access_node = "mynode"
        assert policy.data_access_node == "mynode"
