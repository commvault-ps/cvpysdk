"""Unit tests for cvpysdk/instances/cloudapps/salesforce_instance.py"""

import pytest

from cvpysdk.instances.cainstance import CloudAppsInstance


@pytest.mark.unit
class TestSalesforceInstance:
    """Tests for the SalesforceInstance class."""

    def test_inherits_cloud_apps_instance(self):
        """Test that SalesforceInstance is a subclass of CloudAppsInstance."""
        from cvpysdk.instances.cloudapps.salesforce_instance import SalesforceInstance

        assert issubclass(SalesforceInstance, CloudAppsInstance)

    def test_ca_instance_type_property(self):
        """Test ca_instance_type returns SALESFORCE."""
        from cvpysdk.instances.cloudapps.salesforce_instance import SalesforceInstance

        inst = object.__new__(SalesforceInstance)
        assert inst.ca_instance_type == "SALESFORCE"

    def test_organization_id_property(self):
        """Test organization_id property returns correct value."""
        from cvpysdk.instances.cloudapps.salesforce_instance import SalesforceInstance

        inst = object.__new__(SalesforceInstance)
        inst._properties = {"cloudAppsInstance": {"salesforceInstance": {"sfOrgID": "org123"}}}
        assert inst.organization_id == "org123"

    def test_organization_id_raises_on_missing(self):
        """Test organization_id raises SDKException when not available."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.salesforce_instance import SalesforceInstance

        inst = object.__new__(SalesforceInstance)
        inst._properties = {"cloudAppsInstance": {}}
        with pytest.raises(SDKException):
            _ = inst.organization_id

    def test_login_url_property(self):
        """Test login_url property returns correct value."""
        from cvpysdk.instances.cloudapps.salesforce_instance import SalesforceInstance

        inst = object.__new__(SalesforceInstance)
        inst._properties = {
            "cloudAppsInstance": {
                "salesforceInstance": {"endpoint": "https://login.salesforce.com"}
            }
        }
        assert inst.login_url == "https://login.salesforce.com"

    def test_consumer_id_property(self):
        """Test consumer_id property returns correct value."""
        from cvpysdk.instances.cloudapps.salesforce_instance import SalesforceInstance

        inst = object.__new__(SalesforceInstance)
        inst._properties = {
            "cloudAppsInstance": {"salesforceInstance": {"consumerId": "consumer_abc"}}
        }
        assert inst.consumer_id == "consumer_abc"

    def test_restore_to_file_system_raises_for_non_list_paths(self):
        """Test restore_to_file_system raises SDKException when paths is not a list."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.salesforce_instance import SalesforceInstance

        inst = object.__new__(SalesforceInstance)
        with pytest.raises(SDKException):
            inst.restore_to_file_system(paths="not_a_list")
