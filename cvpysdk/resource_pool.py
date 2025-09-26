# Copyright Commvault Systems, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# --------------------------------------------------------------------------

"""Main file for performing resource pool related operations on CS

ResourcePools , ResourcePool and ResourcePoolTypes are the classes defined in this file

ResourcePools:

        __init__()                          --  initialise object of the ResourcePools class

        _response_not_success()             --  parses through the exception response, and raises SDKException

        _get_resource_pools()               --  returns resource pools details from CS

        has()                               --  Checks whether given resource pool exists in cs or not

        get()                               -- returns ResourcePool object for given name

        delete()                            --  deletes the resource pool from CS

        create()                            --  creates resource pool in CS

        refresh()                           --  Refreshes resource pools associated with cs

ResourcePool:

        __init__()                          --  initialise object of the ResourcePool class

        _response_not_success()             --  parses through the exception response, and raises SDKException

        _get_pool_details()                 --  returns resource pool details from cs

        refresh()                           --  refreshes resource pool details

ResourcePool Attributes:
----------------------------------

    **resource_pool_id**        --  returns Resource pool id

    **resource_pool_type**      --  returns ResourcePoolTypes enum

"""

from .exception import SDKException

import enum

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import requests
    from cvpysdk.commcell import Commcell


class ResourcePoolTypes(enum.Enum):
    """
    Enumeration class representing different types of resource pools.

    This enum is used to define and categorize various resource pool types
    within the application, providing a clear and type-safe way to reference
    specific pool categories throughout the codebase.

    Key Features:
        - Defines distinct resource pool types as enumeration members
        - Ensures type safety and clarity when working with resource pools
        - Facilitates consistent usage of resource pool identifiers

    #ai-gen-doc
    """
    GENERIC = 0
    O365 = 1
    SALESFORCE = 2
    EXCHANGE = 3
    SHAREPOINT = 4
    ONEDRIVE = 5
    TEAMS = 6
    DYNAMICS_365 = 7
    VSA = 8
    FILESYSTEM = 9
    KUBERNETES = 10
    AZURE_AD = 11
    CLOUD_LAPTOP = 12
    FILE_STORAGE_OPTIMIZATION = 13
    DATA_GOVERNANCE = 14
    E_DISCOVERY = 15
    CLOUD_DB = 16
    OBJECT_STORAGE = 17
    GMAIL = 18
    GOOGLE_DRIVE = 19
    GOOGLE_WORKSPACE = 20
    SERVICENOW = 21
    THREATSCAN = 22
    DEVOPS = 23
    RISK_ANALYSIS = 24
    GOOGLE_CLOUD_PLATFORM = 50001


class ResourcePools:
    """
    Class to manage and represent all resource pools within a system.

    This class provides a comprehensive interface for interacting with resource pools,
    including creation, deletion, retrieval, existence checks, and refreshing the pool list.
    It also includes internal mechanisms for handling responses and fetching resource pool data.

    Key Features:
        - Initialize with a Commcell object for context
        - Create new resource pools with specified names and types
        - Delete existing resource pools by name
        - Retrieve resource pool details by name
        - Check for the existence of a resource pool
        - Refresh the list of resource pools to reflect current state
        - Internal handling of unsuccessful responses
        - Internal retrieval of all resource pools

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell') -> None:
        """Initialize a new instance of the ResourcePools class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> resource_pools = ResourcePools(commcell)
            >>> print("ResourcePools instance created successfully")

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._API_GET_ALL_RESOURCE_POOLS = self._services['GET_RESOURCE_POOLS']
        self._API_DELETE_RESOURCE_POOL = self._services['DELETE_RESOURCE_POOL']
        self._API_CREATE_RESOURCE_POOL = self._services['CREATE_RESOURCE_POOL']
        self._pools = {}
        self.refresh()

    def _response_not_success(self, response: 'requests.Response') -> None:
        """Raise an exception if the API response status is not 200 (OK).

        This helper function checks the status of the provided response object, typically 
        obtained from the `requests` Python package, and raises an exception if the status 
        code indicates a failure.

        Args:
            response: The response object returned from an API request.

        #ai-gen-doc
        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_resource_pools(self) -> dict:
        """Retrieve resource pool details from the CommServe (CS).

        Returns:
            dict: A dictionary containing details of all resource pools.

        Raises:
            SDKException: If the resource pool details could not be retrieved.

        #ai-gen-doc
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._API_GET_ALL_RESOURCE_POOLS)
        output = {}
        if flag:
            if response.json() and 'resourcePools' in response.json():
                _resourcepools = response.json()['resourcePools']
                for _pool in _resourcepools:
                    if 'name' in _pool:
                        output.update({_pool['name'].lower(): _pool})
            elif bool(response.json()):
                raise SDKException('ResourcePools', '103')
            return output
        self._response_not_success(response)

    def create(self, name: str, resource_type: 'ResourcePoolTypes', **kwargs: str) -> 'ResourcePool':
        """Create a new resource pool in the CommServe.

        Args:
            name: The name of the resource pool to create.
            resource_type: The type of resource pool, specified as a ResourcePoolTypes enum.
            **kwargs: Additional keyword arguments for resource pool creation.
                For Threat Scan resource pools, you may specify:
                    index_server (str): The name of the index server to associate with the pool.

        Returns:
            ResourcePool: An instance representing the newly created resource pool.

        Raises:
            SDKException: If the resource pool creation fails or if a resource pool with the given name already exists.

        Example:
            >>> pool = resource_pools.create(
            ...     name="ThreatScanPool",
            ...     resource_type=ResourcePoolTypes.THREATSCAN,
            ...     index_server="IndexServer01"
            ... )
            >>> print(f"Created resource pool: {pool}")

        #ai-gen-doc
        """
        if resource_type.value not in [ResourcePoolTypes.THREATSCAN.value]:
            raise SDKException('ResourcePools', '102', 'Resource pool creation is not supported for this resource type')
        if resource_type.value == ResourcePoolTypes.THREATSCAN.value and 'index_server' not in kwargs:
            raise SDKException('ResourcePools', '102', 'Index server name is missing in kwargs')
        if self.has(name=name):
            raise SDKException('ResourcePools', '107')
        _request_json = {
            "resourcePool": {
                "appType": resource_type.value,
                "dataAccessNodes": [],
                "extendedProp": {
                    "exchangeOnePassClientProperties": {}},
                "resourcePool": {
                    "resourcePoolId": 0,
                    "resourcePoolName": name},
                "exchangeServerProps": {
                    "jobResultsDirCredentials": {
                        "userName": ""},
                    "jobResultsDirPath": ""},
                "roleId": None,
                "indexServerMembers": [],
                "indexServer": {
                    "clientId": self._commcell_object.index_servers.get(
                        kwargs.get('index_server')).index_server_client_id if resource_type.value == ResourcePoolTypes.THREATSCAN.value else 0,
                    "clientName": kwargs.get('index_server') if resource_type.value == ResourcePoolTypes.THREATSCAN.value else '',
                    "displayName": kwargs.get('index_server') if resource_type.value == ResourcePoolTypes.THREATSCAN.value else '',
                    "selected": True},
                "accessNodes": {
                    "clientGroups": [],
                    "clients": []}}}
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._API_CREATE_RESOURCE_POOL, _request_json)
        if flag:
            if response.json() and 'error' in response.json():
                _error = response.json()['error']
                if _error.get('errorCode', 0) != 0:
                    raise SDKException('ResourcePools', '102', f'Resource pool creation failed with {_error}')
                self.refresh()
                return self.get(name=name)
            raise SDKException('ResourcePools', '108')
        self._response_not_success(response)

    def delete(self, name: str) -> None:
        """Delete a resource pool from the CommServe (CS) by name.

        Args:
            name: The name of the resource pool to delete.

        Raises:
            SDKException: If the resource pool cannot be found or deletion fails.

        #ai-gen-doc
        """
        if not self.has(name=name):
            raise SDKException('ResourcePools', '104')
        api = self._API_DELETE_RESOURCE_POOL % (self._pools[name.lower()]['id'])
        flag, response = self._cvpysdk_object.make_request('DELETE', api)
        if flag:
            if response.json() and 'error' in response.json():
                _error = response.json()['error']
                if _error.get('errorCode', 0) != 0:
                    raise SDKException('ResourcePools', '102', f'Resource pool deletion failed with {_error}')
                self.refresh()
                return
            raise SDKException('ResourcePools', '106')
        self._response_not_success(response)

    def get(self, name: str) -> 'ResourcePool':
        """Retrieve a ResourcePool object by its name.

        Args:
            name: The name of the resource pool to retrieve.

        Returns:
            ResourcePool: An instance of the ResourcePool class corresponding to the specified name.

        Raises:
            SDKException: If a resource pool with the given name cannot be found.

        #ai-gen-doc
        """
        if not self.has(name):
            raise SDKException('ResourcePools', '104')
        return ResourcePool(commcell_object=self._commcell_object, name=name, pool_id=self._pools[name.lower()]['id'])

    def has(self, name: str) -> bool:
        """Check if a resource pool with the specified name exists in the CommServe.

        Args:
            name: The name of the resource pool to check.

        Returns:
            True if the resource pool exists in the CommServe; False otherwise.

        #ai-gen-doc
        """
        if name.lower() in self._pools:
            return True
        return False

    def refresh(self) -> None:
        """Reload the resource pools associated with the CommServe (CS).

        This method refreshes the internal state of the ResourcePools object, ensuring that 
        any changes to resource pools on the CommServe are reflected in the current instance.

        #ai-gen-doc
        """
        self._pools = {}
        self._pools = self._get_resource_pools()


class ResourcePool:
    """
    Represents a resource pool within a system, providing management and access to pool details.

    This class encapsulates the properties and operations related to a resource pool, including
    initialization with specific identifiers, retrieval and refreshing of pool details, and
    access to pool-specific properties such as ID and type. It also includes internal mechanisms
    for handling unsuccessful responses from operations.

    Key Features:
        - Initialize a resource pool with a commcell object, name, and pool ID
        - Retrieve and refresh resource pool details
        - Handle unsuccessful responses from operations
        - Access resource pool ID and type via properties

    #ai-gen-doc
    """

    def __init__(self, commcell_object: 'Commcell', name: str, pool_id: int) -> None:
        """Initialize a new instance of the ResourcePool class.

        Args:
            commcell_object: An instance of the Commcell class representing the active Commcell connection.
            name: The name of the resource pool.
            pool_id: The unique identifier for the resource pool.

        Example:
            >>> commcell = Commcell('commcell_host', 'username', 'password')
            >>> resource_pool = ResourcePool(commcell, 'MainPool', 12345)

        #ai-gen-doc
        """
        self._commcell_object = commcell_object
        self._update_response_ = commcell_object._update_response_
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._resource_pool_name = name
        self._resource_pool_id = pool_id
        self._resource_details = None
        self._API_GET_POOL_DETAILS = self._services['GET_RESOURCE_POOL_DETAILS']
        self.refresh()

    def _response_not_success(self, response: 'requests.Response') -> None:
        """Raise an exception if the API response status is not 200 (OK).

        This helper function checks the status of the provided response object,
        typically obtained from the `requests` Python package, and raises an
        exception if the response indicates a failure (i.e., status code is not 200).

        Args:
            response: The response object returned from an API request.

        #ai-gen-doc
        """
        raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def _get_pool_details(self) -> dict:
        """Retrieve the details of the resource pool from the CommServe.

        Returns:
            dict: A dictionary containing the resource pool details.

        Raises:
            SDKException: If the details for the resource pool could not be retrieved.

        #ai-gen-doc
        """
        api = self._API_GET_POOL_DETAILS % (self._resource_pool_id)
        flag, response = self._cvpysdk_object.make_request('GET', api)
        if flag:
            if response.json() and 'resourcePool' in response.json():
                return response.json()['resourcePool']
            raise SDKException('ResourcePools', '105')
        self._response_not_success(response)

    def refresh(self) -> None:
        """Reload the details of the resource pool.

        This method updates the internal state of the ResourcePool instance to reflect 
        the latest information from the underlying data source or system.

        #ai-gen-doc
        """
        self._resource_details = None
        self._resource_details = self._get_pool_details()

    @property
    def resource_pool_id(self) -> int:
        """Get the unique identifier (ID) for this resource pool.

        Returns:
            The resource pool ID as an integer.

        #ai-gen-doc
        """
        return int(self._resource_details['resourcePool'].get('resourcePoolId'))

    @property
    def resource_pool_type(self) -> 'ResourcePoolTypes':
        """Get the pool type enum for this resource pool.

        Returns:
            ResourcePoolTypes: The enum value representing the type of this resource pool.

        #ai-gen-doc
        """
        return ResourcePoolTypes(int(self._resource_details['appType']))
