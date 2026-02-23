"""Unit tests for cvpysdk/instances/cloudapps/cloud_storage_instance.py"""

import pytest

from cvpysdk.instances.cainstance import CloudAppsInstance


@pytest.mark.unit
class TestCloudStorageInstance:
    """Tests for the CloudStorageInstance class."""

    def test_inherits_cloud_apps_instance(self):
        """Test that CloudStorageInstance is a subclass of CloudAppsInstance."""
        from cvpysdk.instances.cloudapps.cloud_storage_instance import CloudStorageInstance

        assert issubclass(CloudStorageInstance, CloudAppsInstance)

    def test_properties_default_to_none(self):
        """Test that instance properties default to None after __new__."""
        from cvpysdk.instances.cloudapps.cloud_storage_instance import CloudStorageInstance

        inst = object.__new__(CloudStorageInstance)
        inst._ca_instance_type = None
        inst._host_url = None
        inst._access_keyid = None
        inst._account_name = None
        inst._access_key = None
        inst._server_name = None
        inst._access_node = None

        assert inst._ca_instance_type is None
        assert inst._host_url is None
        assert inst._access_node is None

    def test_restore_in_place_raises_for_non_list(self):
        """Test restore_in_place raises SDKException for non-list paths."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.cloud_storage_instance import CloudStorageInstance

        inst = object.__new__(CloudStorageInstance)
        with pytest.raises(SDKException):
            inst.restore_in_place("not_a_list")

    def test_restore_out_of_place_raises_for_bad_types(self):
        """Test restore_out_of_place raises SDKException for incorrect types."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.cloud_storage_instance import CloudStorageInstance

        inst = object.__new__(CloudStorageInstance)
        with pytest.raises(SDKException):
            inst.restore_out_of_place(
                paths="not_a_list",
                destination_client="client",
                destination_instance_name="inst",
                destination_path="/path",
            )

    def test_restore_using_proxy_raises_for_empty_cloud(self):
        """Test restore_using_proxy raises SDKException when destination_cloud is None."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.cloud_storage_instance import CloudStorageInstance

        inst = object.__new__(CloudStorageInstance)
        with pytest.raises(SDKException):
            inst.restore_using_proxy(
                paths=["/path"],
                destination_client_proxy="proxy_client",
                destination_path="/dest",
                destination_cloud=None,
            )

    def test_restore_using_proxy_raises_for_multiple_vendors(self):
        """Test restore_using_proxy raises SDKException for multiple vendor entries."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.cloud_storage_instance import CloudStorageInstance

        inst = object.__new__(CloudStorageInstance)
        with pytest.raises(SDKException):
            inst.restore_using_proxy(
                paths=["/path"],
                destination_client_proxy="proxy_client",
                destination_path="/dest",
                destination_cloud={"google_cloud": {}, "amazon_s3": {}},
            )

    def test_restore_using_proxy_raises_for_unsupported_vendor(self):
        """Test restore_using_proxy raises SDKException for unsupported cloud vendor."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.cloud_storage_instance import CloudStorageInstance

        inst = object.__new__(CloudStorageInstance)
        with pytest.raises(SDKException):
            inst.restore_using_proxy(
                paths=["/path"],
                destination_client_proxy="proxy_client",
                destination_path="/dest",
                destination_cloud={"unsupported_vendor": {}},
            )

    def test_set_proxy_credential_json_amazon(self):
        """Test _set_proxy_credential_json for Amazon S3."""
        from cvpysdk.instances.cloudapps.cloud_storage_instance import CloudStorageInstance

        inst = object.__new__(CloudStorageInstance)
        dest_cloud = {
            "amazon_s3": {
                "s3_host_url": "s3.amazonaws.com",
                "s3_access_key": "AKID",
                "s3_secret_key": "SECRET",
            }
        }
        inst._set_proxy_credential_json(dest_cloud)
        assert inst._proxy_credential_json["instanceType"] == 5
        assert inst._proxy_credential_json["s3Instance"]["accessKeyId"] == "AKID"
