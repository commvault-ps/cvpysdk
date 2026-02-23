"""Unit tests for cvpysdk/instances/cloudapps/spanner_instance.py"""

import pytest

from cvpysdk.instances.cainstance import CloudAppsInstance


@pytest.mark.unit
class TestGoogleSpannerInstance:
    """Tests for the GoogleSpannerInstance class."""

    def test_inherits_cloud_apps_instance(self):
        """Test that GoogleSpannerInstance is a subclass of CloudAppsInstance."""
        from cvpysdk.instances.cloudapps.spanner_instance import GoogleSpannerInstance

        assert issubclass(GoogleSpannerInstance, CloudAppsInstance)

    def test_instance_type_property(self):
        """Test instance_type returns the ca_instance_type."""
        from cvpysdk.instances.cloudapps.spanner_instance import GoogleSpannerInstance

        inst = object.__new__(GoogleSpannerInstance)
        inst._ca_instance_type = 15
        assert inst.instance_type == 15

    def test_spanner_instance_id_property(self):
        """Test spanner_instance_id returns the google instance id."""
        from cvpysdk.instances.cloudapps.spanner_instance import GoogleSpannerInstance

        inst = object.__new__(GoogleSpannerInstance)
        inst._google_instance_id = "spanner-inst-123"
        assert inst.spanner_instance_id == "spanner-inst-123"

    def test_proxy_client_property(self):
        """Test proxy_client returns the proxy client name."""
        from cvpysdk.instances.cloudapps.spanner_instance import GoogleSpannerInstance

        inst = object.__new__(GoogleSpannerInstance)
        inst._proxy_client = "proxy_client_1"
        assert inst.proxy_client == "proxy_client_1"

    def test_staging_path_property(self):
        """Test staging_path returns the cloud staging path."""
        from cvpysdk.instances.cloudapps.spanner_instance import GoogleSpannerInstance

        inst = object.__new__(GoogleSpannerInstance)
        inst._staging_path = "/staging/path"
        assert inst.staging_path == "/staging/path"

    def test_project_id_property(self):
        """Test project_id returns the cloud project id."""
        from cvpysdk.instances.cloudapps.spanner_instance import GoogleSpannerInstance

        inst = object.__new__(GoogleSpannerInstance)
        inst._project_id = "my-gcp-project"
        assert inst.project_id == "my-gcp-project"
