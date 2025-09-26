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

"""File for operating on a Virtual Server Kubernetes Backupset.

KubernetesBackupset is the only class defined in this file.

KubernetesBackupset:               Derived class from Virtual server Backupset Base
                                    class,representing a Kubernetes Backupset ,
                                    and to perform operations on that Backupset

KubernetesBackupset:

    __init__(
        instance_object,
        backupset_name,
        backupset_id)           --  initialize object of Kubernetes backupset class,
                                    associated with the VirtualServer subclient

    refresh ()                    --  refresh the Backupset associated with the agent

    application_groups()        --   Apllication groups property

"""
from enum import Enum
from json import JSONDecodeError
from typing import *
from cvpysdk.backupsets.vsbackupset import VSBackupset
from cvpysdk.exception import SDKException
from ...subclients.virtualserver.kubernetes import ApplicationGroups


class KubernetesBackupset(VSBackupset):
    """Derived class from Virtual server Backupset Base class.

    Represents a Kubernetes Backupset and to perform operations on that Backupset.

    Attributes:
        _blr_pair_details (dict): Placeholder for BLR pair details.
        _application_groups (ApplicationGroups): Manages application groups within the Kubernetes backupset.

    Usage:
        ```
        k8s_backupset = KubernetesBackupset(instance_object, 'default')
        ```
    """

    def __init__(self, instance_object: object, backupset_name: str, backupset_id: str = None) -> None:
        """Initialise the backupset object.

        Args:
            instance_object (object): Instance object of the Virtual Server.
            backupset_name  (str): Name of the backupset.
            backupset_id    (str, optional): ID of the backupset. Defaults to None.
        """
        self._blr_pair_details = None
        super().__init__(instance_object, backupset_name, backupset_id)
        self._application_groups = None

    def refresh(self) -> None:
        """Refresh the properties of the Backupset."""
        super().refresh()
        self._application_groups = None

    @property
    def application_groups(self) -> ApplicationGroups:
        """Returns the ApplicationGroups object associated with this backupset.

        Returns:
            ApplicationGroups: The ApplicationGroups object.

        Usage:
            ```
            app_groups = k8s_backupset.application_groups
            ```
        """
        if self._application_groups is None:
            self._application_groups = ApplicationGroups(self)
        return self._application_groups
