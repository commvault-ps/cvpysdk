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
Module for operating on a Virtual Server Morpheus Server Instance.

This module defines the MorpheusInstance class, which is a subclass of
VirtualServerInstance. It provides functionality specific to managing
Morpheus virtual server instances within the Commvault framework.

Classes:
    MorpheusInstance -- Represents a Morpheus virtual server instance and
                         provides methods to get and set instance properties.
"""

from ..vsinstance import VirtualServerInstance


class MorpheusInstance(VirtualServerInstance):
    """
    Class for representing a Morpheus instance of the Virtual Server agent.

    This class extends the VirtualServerInstance base class and provides
    additional functionality specific to Morpheus server instances.

    Attributes:
        _vendor_id (int): Vendor ID for Morpheus (fixed as 27).
        _server_name (list): List containing the name of the associated client.
        _server_host_name (list): List containing the host name of the associated client.
    """

    def __init__(self, agent, instance_name, instance_id=None):
        """
        Initializes the MorpheusInstance object.

        Args:
            agent (object): Instance of the Agent class.
            instance_name (str): Name of the instance.
            instance_id (int, optional): ID of the instance. Defaults to None.

        Sets:
            _vendor_id: Vendor ID specific to Morpheus.
            _server_name: Name of the associated client.
            _server_host_name: Host name of the associated client.
        """
        super(MorpheusInstance, self).__init__(agent, instance_name, instance_id)
        self._vendor_id = 27
        self._server_name = [
            self._virtualserverinstance['associatedClients']['memberServers'][0]['client'].get('clientName')
        ]
        self._server_host_name = [
            self._virtualserverinstance['associatedClients']['memberServers'][0]['client'].get('hostName')
        ]

    def _get_instance_properties(self):
        """
        Retrieves the properties of the Morpheus instance.

        This method overrides the base class method to include Morpheus-specific
        instance properties.

        Raises:
            SDKException: If the response is not empty or not successful.
        """
        super(MorpheusInstance, self)._get_instance_properties()

    def _get_instance_properties_json(self):
        """
        Constructs and returns the JSON representation of the instance properties.

        Returns:
            dict: Dictionary containing all relevant instance properties.
        """
        instance_json = {
            "instanceProperties": {
                "isDeleted": False,
                "instance": self._instance,
                "instanceActivityControl": self._instanceActivityControl,
                "virtualServerInstance": {
                    "vsInstanceType": self._virtualserverinstance['vsInstanceType'],
                    "associatedClients": self._virtualserverinstance['associatedClients']
                }
            }
        }
        return instance_json

    @property
    def server_host_name(self):
        """
        Returns the host name(s) of the associated Morpheus server.

        Returns:
            list: List of host names.
        """
        return self._server_host_name

    @server_host_name.setter
    def server_host_name(self, value):
        """
        Sets the host name(s) of the Morpheus server.

        Args:
            value (list): List of host names to set.
        """
        self._server_host_name = value

    @property
    def server_name(self):
        """
        Returns the name(s) of the associated Morpheus server.

        Returns:
            list: List of server names.
        """
        return self._server_name
