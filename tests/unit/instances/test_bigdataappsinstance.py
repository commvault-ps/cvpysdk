"""Unit tests for cvpysdk/instances/bigdataappsinstance.py"""

from unittest.mock import MagicMock

import pytest

from cvpysdk.instance import Instance


@pytest.mark.unit
class TestBigDataAppsInstance:
    """Tests for the BigDataAppsInstance class."""

    def test_inherits_instance(self):
        """Test that BigDataAppsInstance is a subclass of Instance."""
        from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance

        assert issubclass(BigDataAppsInstance, Instance)

    def test_new_returns_couchbase_for_type_17(self):
        """Test __new__ returns CouchbaseInstance for cluster type 17."""
        from cvpysdk.instances.bigdataapps.couchbaseinstance import CouchbaseInstance
        from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "instanceProperties": [
                {
                    "distributedClusterInstance": {"clusterType": 17},
                }
            ]
        }
        agent_object._commcell_object.request.return_value = response

        obj = BigDataAppsInstance.__new__(BigDataAppsInstance, agent_object, "test", 1)
        assert isinstance(obj, CouchbaseInstance)

    def test_new_returns_mongodb_for_type_8(self):
        """Test __new__ returns MongoDBInstance for cluster type 8."""
        from cvpysdk.instances.bigdataapps.mongodbinstance import MongoDBInstance
        from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "instanceProperties": [
                {
                    "distributedClusterInstance": {"clusterType": 8},
                }
            ]
        }
        agent_object._commcell_object.request.return_value = response

        obj = BigDataAppsInstance.__new__(BigDataAppsInstance, agent_object, "test", 2)
        assert isinstance(obj, MongoDBInstance)

    def test_new_returns_yugabyte_for_type_19(self):
        """Test __new__ returns YugabyteInstance for cluster type 19."""
        from cvpysdk.instances.bigdataapps.yugabyteinstance import YugabyteInstance
        from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "instanceProperties": [
                {
                    "distributedClusterInstance": {"clusterType": 19},
                }
            ]
        }
        agent_object._commcell_object.request.return_value = response

        obj = BigDataAppsInstance.__new__(BigDataAppsInstance, agent_object, "test", 3)
        assert isinstance(obj, YugabyteInstance)

    def test_new_returns_base_for_unknown_type(self):
        """Test __new__ returns BigDataAppsInstance for unknown cluster type."""
        from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {
            "instanceProperties": [
                {
                    "distributedClusterInstance": {"clusterType": 999},
                }
            ]
        }
        agent_object._commcell_object.request.return_value = response

        obj = BigDataAppsInstance.__new__(BigDataAppsInstance, agent_object, "test", 4)
        assert type(obj) is BigDataAppsInstance

    def test_new_raises_on_bad_response(self):
        """Test __new__ raises SDKException for empty response."""
        from cvpysdk.exception import SDKException
        from cvpysdk.instances.bigdataappsinstance import BigDataAppsInstance

        agent_object = MagicMock()
        response = MagicMock()
        response.json.return_value = {}
        agent_object._commcell_object.request.return_value = response

        with pytest.raises(SDKException):
            BigDataAppsInstance.__new__(BigDataAppsInstance, agent_object, "test", 5)
