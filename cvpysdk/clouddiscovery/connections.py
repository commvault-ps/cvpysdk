# -*- coding: utf-8 -*-

# --------------------------------------------------------------------------
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

"""
Module for managing Cloud Discovery connections.

Classes:
    Connection:
        Represents a cloud discovery connection to a specific asset provider.

        Methods:
            __init__()              - Initialize a Connection instance.
            get_configs()           - Get all configuration name-value pairs for this connection.
            get_resources()         - Get all resources discovered by this connection as name-value pairs.
            update_connection()     - Update the connection configuration.
            start_discovery()       - Start the discovery process for this connection.

        Properties:
            credential_name           - Get the credential ID for this connection.
            asset_provider          - Get the asset provider for this connection.

    Connections:
        Manager class for handling multiple cloud discovery connections.

        Methods:
            __init__()              - Initialize the Connections manager.
            add_connection()        - Add a new connection with the specified credential and configuration.
            delete_connection()     - Delete an existing connection by credential ID.
            get_connection()        - Get a connection by credential ID.
            has_connection()        - Check if a connection exists for the given credential ID.
            refresh()               - Refresh the connections cache by fetching latest data.
            _get_all_connections()  - Internal method to retrieve all connections from the backend.

        Properties:
            all_connections         - Get all connections managed by this instance.
"""

from typing import Dict, Optional, TYPE_CHECKING, List

from .constants import AssetProvider
from .resources import DiscoveredResource

if TYPE_CHECKING:
    from ..commcell import Commcell

class Connection:
    """Represents a cloud discovery connection to a specific asset provider.
    
    This class manages the configuration and operations for a single cloud
    discovery connection, including credential management and resource discovery.
    """


    def __init__(self, commcell: 'Commcell',
                 credential_name: str,
                 asset_provider: AssetProvider) -> None:
        """Initialize a Connection instance.

        Args:
            commcell: The Commcell object for API operations
            credential_name: Unique identifier for the credential
            asset_provider: The cloud asset provider type

        Returns:
            None

        Example:
            >>> commcell = Commcell()
            >>> provider = AssetProvider.AWS
            >>> connection = Connection(commcell, "cred123", provider)
        """
        self._commcell = commcell
        self._credential_name = credential_name
        self._asset_provider = asset_provider
        credential = self._commcell.credentials.get(self._credential_name)
        self._credential_id = credential.credential_id if credential is not None else None



    @property
    def credential_id(self) -> int:
        """Get the credential ID for this connection.
        
        Returns:
            The unique credential identifier
        """
        return self._credential_id

    @property
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider for this connection.
        
        Returns:
            The AssetProvider enum value
        """
        return self._asset_provider

    def get_configs(self) -> List[Dict[str, str]]:
        """Get all configuration name-value pairs (regions/subscriptions) for this connection.
        
        Returns:
            Dictionary containing configuration key-value pairs
            
        Raises:
            NotImplementedError: This method is not yet implemented

        Example:
            >>> connection = Connections().get_connection("cred123")
            >>> configs = connection.get_configs()
            >>> print(configs)
            [{'region': 'us-east-1'}, {'region': 'us-west-2'}]
            >>> configs = connection.get_configs()
            >>> print(configs)
            [{'subscription': 'sub-123'}, {'subscription': 'sub-456'}]
        """
        raise NotImplementedError("get_configs method is not yet implemented")

    def get_resources(self) -> List[DiscoveredResource]:
        """Get all resources discovered by this connection as name-value pairs.
        
        Returns:
            Dictionary containing resource name-value pairs
            
        Raises:
            NotImplementedError: This method is not yet implemented

        Example:
            >>> resources = connection.get_resources()
            >>> for resource in resources:
            ...     print(resource.name, resource.asset_type, resource.workload_type)
            vm2 VirtualMachine COMPUTE
        """
        raise NotImplementedError("get_resources method is not yet implemented")

    def update_connection(
        self, 
        include_all_configs: bool = False, 
        config_list: Optional[Dict[str, str]] = None
    ) -> bool:
        """Update the connection configuration.

        Args:
            include_all_configs: Whether to include all available configurations (regions/subscriptions)
            config_list: Specific configurations (regions/subscriptions) to update (optional)

        Returns:
            True if update was successful, False otherwise

        Example:
            >>> connection = Connections().get_connection("cred123")
            >>> connection.update_connection(include_all_configs=True)
            True
            >>> connection.update_connection(config_list={"region": "us-east-1"})
            True
            >>> connection.update_connection(config_list={"subscription": "sub-123"})
            True

        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError("update_connection method is not yet implemented")

    def start_discovery(self) -> bool:
        """Start the discovery process for this connection.
        
        Returns:
            True if discovery started successfully, False otherwise
            
        Raises:
            NotImplementedError: This method is not yet implemented

        Example:
            >>> connection = Connections().get_connection("cred123")
            >>> connection.start_discovery()
            True
        """
        raise NotImplementedError("start_discovery method is not yet implemented")


class Connections:
    """Manager class for handling multiple cloud discovery connections.
    
    This class provides methods to manage a collection of Connection objects,
    including adding, deleting, and retrieving connections by credential ID.
    """

    def __init__(self, commcell: 'Commcell', asset_provider: AssetProvider = None) -> None:
        """
        Initialize the Connections manager.
        Args:
            commcell: The Commcell object to which this connection manager belongs
        """
        self._commcell = commcell
        self._connections: List[Connection] = []
        self._is_loaded = False

    def add_connection(
        self,
        credential_name: str,
        config_list: Dict[str, str],
        start_discovery: bool = True
    ) -> Connection:
        """Add a new connection with the specified credential and configuration.

        Args:
            credential_name: Unique identifier for the credential
            config_list: Configuration parameters for the connection
            start_discovery: Whether to start discovery immediately after adding

        Returns:
            The newly created Connection object

        Example:
            >>> instance = Connections()
            >>> conn = instance.add_connection("cred_123", {"host": "localhost", "port": "5432"})
            >>> print(conn.credential_id)
            123

        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError("add_connection method is not yet implemented")

    def delete_connection(self, credential_name: str) -> bool:
        """Delete an existing connection by credential name.

        Args:
            credential_name: The credential name of the connection to delete

        Returns:
            True if deletion was successful, False otherwise

        Example:
            >>> connection_manager = Connections()
            >>> success = connection_manager.delete_connection("cred_123")
            >>> print(success)
            True

        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError("delete_connection method is not yet implemented")

    def get_connection(self, credential_name: str) -> Optional[Connection]:
        """Get a connection by credential name.

        Args:
            credential_name: The credential name to look up

        Returns:
            The Connection object if found, None otherwise

        Raises:
            NotImplementedError: This method is not yet implemented

        Example:
            >>> connection_manager = Connections()
            >>> conn = connection_manager.get_connection("cred_123")
            >>> if conn:
            ...     print(conn.credential_id)
            123
        """
        raise NotImplementedError("get_connection method is not yet implemented")

    def has_connection(self, credential_name: str) -> bool:
        """Check if a connection exists for the given credential name.

        Args:
            credential_name: The credential name to check

        Returns:
            True if connection exists, False otherwise

        Raises:
            NotImplementedError: This method is not yet implemented

        Example:
            >>> connection_manager = Connections()
            >>> exists = connection_manager.has_connection("cred_123")
            >>> print(exists)
            True
        """
        raise NotImplementedError("has_connection method is not yet implemented")

    def _get_all_connections(self) -> List[Connection]:
        """Internal method to retrieve all connections from the backend.
        
        This is a private method that handles the actual data retrieval
        from the underlying storage or API.
        
        Returns:
            List of Connection objects
            
        Raises:
            NotImplementedError: This method is not yet implemented

        Example:
            >>> connection_manager = Connections()
            >>> connections = connection_manager._get_all_connections()
            >>> for conn in connections:
            ...     print(conn.credential_id)
            123
            456
        """
        raise NotImplementedError("_get_all_connections method is not yet implemented")

    def refresh(self) -> None:
        """Refresh the connections cache by fetching latest data.
        
        This method updates the internal connections dictionary with
        the most recent data from the backend.
        
        Raises:
            NotImplementedError: This method is not yet implemented

        Example:
            >>> connection_manager = Connections()
            >>> connection_manager.refresh()
        """
        raise NotImplementedError("refresh method is not yet implemented")


    @property
    def all_connections(self) -> List[Connection]:
        """Get all connections managed by this instance.

        Returns:
            List of Connection objects

        Example:
            >>> instance = Connections()
            >>> all_conns = instance.all_connections
            >>> for conn in all_conns:
            ...     print(conn.credential_id, conn.asset_provider)
            123 AWS
            456 AZURE
        """
        if not self._is_loaded:
            self.refresh()
        return self._connections.copy()