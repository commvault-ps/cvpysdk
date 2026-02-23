"""Unit tests for cvpysdk/instances/cloudapps/amazon_instance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instances.cloudapps.cloud_database_instance import CloudDatabaseInstance


@pytest.mark.unit
class TestAmazonRDSInstance:
    """Tests for the AmazonRDSInstance class."""

    def test_inherits_cloud_database_instance(self):
        """Test that AmazonRDSInstance is a subclass of CloudDatabaseInstance."""
        from cvpysdk.instances.cloudapps.amazon_instance import AmazonRDSInstance

        assert issubclass(AmazonRDSInstance, CloudDatabaseInstance)

    def test_process_browse_response_success(self):
        """Test _process_browse_response returns snapshot list on success."""
        from cvpysdk.instances.cloudapps.amazon_instance import AmazonRDSInstance

        inst = object.__new__(AmazonRDSInstance)
        response = MagicMock()
        response.json.return_value = {"snapList": [{"id": "snap-1"}]}

        result = inst._process_browse_response(True, response)
        assert result == [{"id": "snap-1"}]

    def test_process_browse_response_raises_on_failure(self):
        """Test _process_browse_response raises SDKException on failed flag."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.amazon_instance import AmazonRDSInstance

        inst = object.__new__(AmazonRDSInstance)
        with pytest.raises(SDKException):
            inst._process_browse_response(False, "error")

    def test_process_browse_response_raises_on_missing_snaplist(self):
        """Test _process_browse_response raises SDKException when snapList missing."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.cloudapps.amazon_instance import AmazonRDSInstance

        inst = object.__new__(AmazonRDSInstance)
        response = MagicMock()
        response.json.return_value = {"other": "data"}
        with pytest.raises(SDKException):
            inst._process_browse_response(True, response)


@pytest.mark.unit
class TestAmazonRedshiftInstance:
    """Tests for the AmazonRedshiftInstance class."""

    def test_inherits_cloud_database_instance(self):
        """Test that AmazonRedshiftInstance is a subclass of CloudDatabaseInstance."""
        from cvpysdk.instances.cloudapps.amazon_instance import AmazonRedshiftInstance

        assert issubclass(AmazonRedshiftInstance, CloudDatabaseInstance)

    def test_process_browse_response_success(self):
        """Test _process_browse_response returns snapshot list on success."""
        from cvpysdk.instances.cloudapps.amazon_instance import AmazonRedshiftInstance

        inst = object.__new__(AmazonRedshiftInstance)
        response = MagicMock()
        response.json.return_value = {"snapList": [{"id": "snap-2"}]}

        result = inst._process_browse_response(True, response)
        assert result == [{"id": "snap-2"}]


@pytest.mark.unit
class TestAmazonDocumentDBInstance:
    """Tests for the AmazonDocumentDBInstance class."""

    def test_inherits_cloud_database_instance(self):
        """Test that AmazonDocumentDBInstance is a subclass of CloudDatabaseInstance."""
        from cvpysdk.instances.cloudapps.amazon_instance import AmazonDocumentDBInstance

        assert issubclass(AmazonDocumentDBInstance, CloudDatabaseInstance)


@pytest.mark.unit
class TestAmazonDynamoDBInstance:
    """Tests for the AmazonDynamoDBInstance class."""

    def test_inherits_cloud_database_instance(self):
        """Test that AmazonDynamoDBInstance is a subclass of CloudDatabaseInstance."""
        from cvpysdk.instances.cloudapps.amazon_instance import AmazonDynamoDBInstance

        assert issubclass(AmazonDynamoDBInstance, CloudDatabaseInstance)
