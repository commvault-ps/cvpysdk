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
Module for cloud discovery operations across different asset providers.

Classes:
    CloudDiscovery:
        Base class for cloud discovery operations.

        Methods:
            __init__()          - Initialize the CloudDiscovery instance.
            estimate_cost()     - Estimate the cost of discovered resources and protection plans.

        Properties:
            asset_provider      - Get the asset provider for this cloud discovery instance.
            connections         - Get the connections manager for this cloud discovery instance.
            resources           - Get the resources manager for this cloud discovery instance.
            credentials         - Get the credentials for this cloud discovery instance.

    AzureDiscovery:
        Azure-specific cloud discovery implementation.

        Methods:
            __init__()          - Initialize the AzureDiscovery instance.
            estimate_cost()     - Estimate the cost of discovered resources and protection plans.

        Properties:
            asset_provider      - Get the asset provider for this Azure discovery instance.

    AWSDiscovery:
        AWS-specific cloud discovery implementation.

        Methods:
            __init__()          - Initialize the AWSDiscovery instance.
            estimate_cost()     - Estimate the cost of discovered resources and protection plans.

        Properties:
            asset_provider      - Get the asset provider for this AWS discovery instance.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, TYPE_CHECKING
from .constants import AssetProvider
from .connections import Connections
from .resources import DiscoveredResources

if TYPE_CHECKING:
    from ..commcell import Commcell
    from ..credential_manager import Credentials



class CloudDiscovery(ABC):
    """Base class for cloud discovery operations.
    
    This abstract base class provides the common interface for cloud discovery
    operations across different asset providers. It manages connections, resources,
    and credential management for cloud environments.
    """

    def __init__(self, commcell:'Commcell') -> None:
        """Initialize the CloudDiscovery instance.
        
        Args:
            commcell: The Commcell object for API operations
        """
        self._commcell = commcell
        self._connections = Connections(commcell)
        self._resources = DiscoveredResources(commcell)
        self._credentials = commcell.credentials

    @property
    @abstractmethod
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider for this cloud discovery instance.
        
        Returns:
            The AssetProvider enum value
        """
        pass

    @property
    def connections(self) -> Connections:
        """Get the connections manager for this cloud discovery instance.
        
        Returns:
            The Connections manager object
        """
        return self._connections

    @property
    def resources(self) -> DiscoveredResources:
        """Get the resources manager for this cloud discovery instance.
        
        Returns:
            The DiscoveredResources manager object
        """
        return self._resources

    @property
    def credentials(self) -> 'Credentials':
        """Get the credentials for this cloud discovery instance.
        
        Returns:
            The credential manager object or None
        """
        return self._credentials



    @abstractmethod
    def estimate_cost(self) -> Dict[str, Any]:
        """Estimate the cost of discovered resources and protection plans.

        This method should be implemented by each cloud provider to provide
        cost estimation specific to their pricing models and resource types.

        Args:
            None

        Returns:
            Dictionary containing cost estimation details. Uses Any for values
            to accommodate varying cost structures across different cloud providers
            (numeric costs, nested dictionaries, lists of cost breakdowns, etc.)

        Raises:
            NotImplementedError: Must be implemented by derived classes
        """
        pass





class AzureDiscovery(CloudDiscovery):
    """Azure cloud discovery implementation.
    
    This class provides Azure-specific cloud discovery operations including
    resource discovery, connection management, and cost estimation using
    Azure pricing models.
    """

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize the AzureDiscovery instance.
        
        Args:
            commcell: The Commcell object for API operations
        """
        super().__init__(commcell)

    @property
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider for Azure discovery.
        
        Returns:
            AssetProvider.AZURE
        """
        return AssetProvider.AZURE

    def estimate_cost(self) -> Dict[str, Any]:
        """Estimate the cost of Azure resources and protection plans.

        Provides cost estimation for Azure resources including virtual machines,
        storage accounts, databases, and associated Commvault protection costs.

        Returns:
            Dictionary containing Azure cost estimation details including:
                - Resource costs by type
                - Protection plan costs
                - Total estimated monthly cost
                - Cost breakdown by region

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('webconsole', 'user', 'password')
            >>> azure_manager = AzureDiscovery(commcell)
            >>> cost_estimate = azure_manager.estimate_cost()
            >>> print(f"Total monthly cost: ${cost_estimate['total_monthly_cost']}")
            Total monthly cost: $1250.00
            >>> print(f"VM costs: ${cost_estimate['vm_costs']}")
            VM costs: $800.00

        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError("Azure cost estimation is not yet implemented")


class AWSDiscovery(CloudDiscovery):
    """AWS cloud discovery implementation.
    
    This class provides AWS-specific cloud discovery operations including
    resource discovery, connection management, and cost estimation using
    AWS pricing models.
    """

    def __init__(self, commcell: 'Commcell') -> None:
        """Initialize the AWSDiscovery instance.
        
        Args:
            commcell: The Commcell object for API operations
        """
        super().__init__(commcell)

    @property
    def asset_provider(self) -> AssetProvider:
        """Get the asset provider for AWS discovery.
        
        Returns:
            AssetProvider.AWS
        """
        return AssetProvider.AWS


    def estimate_cost(self) -> Dict[str, Any]:
        """Estimate the cost of AWS resources and protection plans.

        Provides cost estimation for AWS resources including EC2 instances,
        S3 storage, RDS databases, and associated Commvault protection costs.

        Returns:
            Dictionary containing AWS cost estimation details including:
                - Resource costs by type
                - Protection plan costs
                - Total estimated monthly cost
                - Cost breakdown by region

        Example:
            >>> from cvpysdk.commcell import Commcell
            >>> commcell = Commcell('webconsole', 'user', 'password')
            >>> aws_manager = AWSDiscovery(commcell)
            >>> cost_estimate = aws_manager.estimate_cost()
            >>> print(f"Total monthly cost: ${cost_estimate['total_monthly_cost']}")
            Total monthly cost: $1250.50

        Raises:
            NotImplementedError: This method is not yet implemented
        """
        raise NotImplementedError("AWS cost estimation is not yet implemented")

