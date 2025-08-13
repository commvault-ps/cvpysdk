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

"""Main file for performing Cleanroom Target specific operations.

CleanroomTargets and CleanroomTarget are 2 classes defined in this file.

CleanroomTargets:     Class for representing all the cleanroom targets

CleanroomTarget:      Class for a single cleanroom target selected, and to perform operations on that cleanroom target


cleanroomTargets:
    __init__()                   --  initialize object of CleanroomTargets class

    __str__()                   --  returns all the Cleanroom Targets

    _get_cleanroom_targets()     -- Gets all the cleanroom targets

    has_cleanroom_target()       -- Checks if a target is present in the commcell.

    get()                        --  returns the cleanroom target class object of the input target name

    refresh()                   --  refresh the targets present in the client

    create()                    --  creates a cleanroom target with the specified payload

    populate_payload()        --  builds the payload with the required fields for creating a cleanroom target

cleanroomTargets Attributes
--------------------------

    **all_targets**             --  returns the dictionary consisting of all the targets that are
    present in the commcell and their information such as id and name

CleanroomTarget:
    __init__()                   --   initialize object of CleanroomTarget with the specified cleanroom target name

    _get_cleanroom_target_id()   --   method to get the cleanroom target id

    _get_cleanroom_target_properties()  --   get the properties of this recovery target

    _delete_cleanroom_target()    -- Deletes the cleanroom target

    delete()                     -- Deletes the cleanroom target

    refresh()                   --   refresh the object properties

CleanroomTarget Attributes
--------------------------

    **cleanroom_target_id**      -- Returns the id of the cleanroom target
    **cleanroom_target_name**    -- Returns the name of the cleanroom Target
    **destination_hypervisor**  -- Returns the name of destination hypervisor
    **vm_prefix**               -- Returns the prefix of the vm name
    **destination_host**        -- Returns the destination host
    **storage_account**          -- Returns the storage_account host
    **policy_type**             -- Returns the policy type
    **application_type**          -- Returns the application type
    **restore_as_managed_vm**   -- Returns the restore_as_managed_vm
    **region**                  -- Returns the region
    **expiration_time**         -- Returns the _expiration_time
    **vm_suffix**               -- Returns the vm_suffix
    **vm_prefix**               -- Returns the vm_prefix
    **access_node**             -- Returns the access_node
    **access_node_client_group** -- Returns the access_node_client_group

"""
from __future__ import absolute_import
from __future__ import unicode_literals

from cvpysdk.exception import SDKException
from json.decoder import JSONDecodeError


class CleanroomTargets:

    """Class for representing all the Cleanroom targets"""

    def __init__(self, commcell_object):
        """Initialize object of the CleanroomTargets class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._RECOVERY_TARGETS_API = self._services['GET_ALL_RECOVERY_TARGETS']
        self._TARGET_URL = self._services['CREATE_RUNBOOK_TARGET']

        self._cleanroom_targets = None
        self.refresh()

    def __str__(self):
        """Representation string consisting of all targets .

            Returns:
                str     -   string of all the targets

        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'CleanroomTargets')

        for index, cleanroom_target in enumerate(self._cleanroom_targets):
            sub_str = '{:^5}\t{:20}\n'.format(
                index + 1,
                cleanroom_target
            )
            representation_string += sub_str

        return representation_string.strip()

    def _get_cleanroom_targets(self):
        """Gets all the cleanroom targets.

            Returns:
                dict - consists of all targets in the client
                    {
                         "target1_name": target1_id,
                         "target2_name": target2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_TARGETS_API)
        if flag:
            if response.json() and 'recoveryTargets' in response.json():
                cleanroom_target_dict = {}
                for cleanroomTarget in response.json()['recoveryTargets']:
                    if cleanroomTarget['applicationType'] == "CLEAN_ROOM":
                        temp_name = cleanroomTarget['name'].lower()
                        cleanroom_target_dict[temp_name] = str(cleanroomTarget['id'])

                return cleanroom_target_dict
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def all_targets(self):
        """Returns dict of all the targets.

         Returns dict    -   consists of all targets

                {
                    "target1_name": target1_id,

                    "target2_name": target2_id
                }

        """
        return self._cleanroom_targets

    def has_cleanroom_target(self, target_name):
        """Checks if a target is present in the commcell.

            Args:
                target_name (str)  --  name of the target

            Returns:
                bool - boolean output whether the target is present in commcell or not

            Raises:
                SDKException:
                    if type of the target name argument is not string

        """
        if not isinstance(target_name, str):
            raise SDKException('Target', '101')

        return self._cleanroom_targets and target_name.lower() in self._cleanroom_targets

    def get(self, cleanroom_target_name):
        """Returns a target object.

            Args:
                cleanroom_target_name (str)  --  name of the target

            Returns:
                object - instance of the target class for the given target name

            Raises:
                SDKException:
                    if type of the target name argument is not string

                    if no target exists with the given name

        """
        if not isinstance(cleanroom_target_name, str):
            raise SDKException('Target', '101')
        else:
            cleanroom_target_name = cleanroom_target_name.lower()

            if self.has_cleanroom_target(cleanroom_target_name):
                return CleanroomTarget(
                    self._commcell_object, cleanroom_target_name, self.all_targets[cleanroom_target_name])

            raise SDKException('RecoveryTarget', '102', 'No target exists with name: {0}'.format(cleanroom_target_name))

    def refresh(self):
        """Refresh the cleanroom targets"""
        self._cleanroom_targets = self._get_cleanroom_targets()

    def create(self, payload=dict()):
        """Creates a cleanroom target.

            Args:
                target_name (str)  --  name of the target
                payload (dict)  --  payload for creating the target

            Returns:
                Response (dict) - response of the request

                        {
                            "id": 1234567890,
                            "name": "target_name"
                        }

            Raises:
                SDKException:
                    if payload is not a dictionary
                    if API response is empty
                    if API response is not success

        """
        if not isinstance(payload, dict):
            raise SDKException('RecoveryTarget', '101', 'Payload must be a dictionary')
        flag, response = self._cvpysdk_object.make_request('POST', self._TARGET_URL, payload=payload)

        if flag:
            try:
                response_json = response.json()
                if not response_json:
                    raise ValueError('Response', '102', 'Empty response received from the server')

                if "id" in response_json:
                    return response_json
                else:
                    raise KeyError('Response', '102', 'Target ID not found in the response')
            except JSONDecodeError:
                raise ValueError('Response', '102', 'Invalid response received from the server.')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def populate_payload(self, target, region, node=None):
        """Builds the payload with the required fields for creating a cleanroom target.

            Args:
                target (dict)  --  target payload to be populated
                node (dict)  --  access node details to be populated
                                Optional when using existing target or existing hypervisor
                region (dict)  --  region details to be populated

            Returns:
                dict - populated payload

            Sample format for target input to be upopulated in payload:

                If using existing target:
                target = {
                    "target_id": 1234567890,
                    "target_name": "Cleanroom_Target",
                    "target_vendor": "AZURE_V2",
                    }

                If creating a new target with existing hypervisor:
                target = {
                    "target_name": "Cleanroom_Target",
                    "target_vendor": "AZURE_V2",
                    "hypervisor_id": 1234567890,
                    "hypervisor_name": "Hypervisor01",
                    }

                If creating a new target with existing credentials:
                target = {
                    "target_name": "Cleanroom_Target",
                    "target_vendor": "AZURE_V2",
                    "credentials_id": 1234567890,
                    "credentials_name": "Azure_Credentials",
                    "subscription_id": "<subscription_id>",
                    }
            Sample format for access node input to be populated in payload:
                If using existing access node:
                node = {
                    "access_node_id": 1234567890,
                    "access_node_type": 3  # 3 for Access Node, 28 for Access Node Group
                }

            Sample format for region input to be populated in payload:
                region = {
                    "guid": "eastus (Commcell)",  # Example region
                    "name": "US East"
                }
            Raises:
                SDKException:
                    if target input is empty
                    if target name is not a string
        """
        if not isinstance(target['target_name'], str):
            raise SDKException('RecoveryTarget', '101', 'Missing or invalid target name')
        api_payload = {
                            "options": {
                            "region": region if region else {},
                            "accessNode": {}
                            }
                        }
        #Populate the payload with access node details
        if node.get('access_node_id') is not None:  #Using existing access node or access node group
            access_node_entity = {
                "id": node.get('access_node_id', 0),
                "name": node.get('access_node_name', 'string'),
                "type": node.get('access_node_type', 3)
            }
            api_payload['options']['accessNode'].update(access_node_entity)
        if not target:
            raise SDKException('RecoveryTarget', '101', 'Target payload cannot be empty')
        elif target.get('target_id') is not None and target.get('target_id') > 0 :  #Using existing target
            target_entity = {
                "entity": {
                "id": target.get('target_id', 0),
                "name": target.get('target_name', 'string')
                }
            }
            api_payload.update(target_entity)
        else:
            options = {
                        "vendor": target.get('target_vendor', 'AZURE_V2')
                    }
            api_payload['options'].update(options)
            if target.get("target_id") == 0 or target.get("target_id") == "":
                if target.get("hypervisor_id") is not None:  # Using existing hypervisor to create new target
                    existing_hypervisor = {
                        "hypervisor": {
                            "entity": {
                                "id": target.get('hypervisor_id', 0),
                                "name": target.get('hypervisor_name', 'string')
                            }
                        }
                    }
                    access_node_entity = {
                        "id": 0,
                        "type": 28
                    }
                    api_payload['options'].update(existing_hypervisor)
                    api_payload['options']['accessNode'].update(access_node_entity)
                elif target.get("credentials_id") is not None:  #Using existing credentials to create new hypervisor for the target
                    new_hypervisor = {
                        "hypervisor": {
                            "optionsAzure": {
                                "credentials": {
                                    "id": target.get('credentials_id', 0),
                                    "name": target.get('credentials_name', 'string')
                                },
                            "skipCredentialValidation": False,
                            "subscriptionId": target.get('subscription_id', '<subscription_id>'),
                            "useManagedIdentity": False
                            }
                        }
                    }
                    options.update(new_hypervisor)
                    api_payload['options'].update(options)
        return api_payload


class CleanroomTarget:
    """Class for performing target operations"""

    def __init__(self, commcell_object, cleanroom_target_name, cleanroom_target_id=None):
        """Initialize the instance of the CleanroomTarget class.

            Args:
                commcell_object   (object)    --  instance of the Commcell class

                cleanroom_target_name      (str)       --  name of the target

                cleanroom_target_id        (str)       --  id of the target

        """
        self._commcell_object = commcell_object

        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._services = commcell_object._services
        self._update_response_ = commcell_object._update_response_
        self._cleanroom_target_name = cleanroom_target_name.lower()

        if cleanroom_target_id:
            # Use the target id mentioned in the arguments
            self._cleanroom_target_id = str(cleanroom_target_id)
        else:
            # Get the target id if target id is not provided
            self._cleanroom_target_id = self._get_cleanroom_target_id()
        self._RECOVERY_TARGET_API = self._services['GET_RECOVERY_TARGET'] % self._cleanroom_target_id

        self._cleanroom_target_properties = None

        self._policy_type = None
        self._application_type = None
        self._destination_hypervisor = None
        self._access_node = None
        self._access_node_client_group = None
        self._instance = None
        self._users = []
        self._user_groups = []
        self._vm_prefix = ''
        self._vm_suffix = ''
        self._expiration_time = None

        self._region = None
        self._availability_zone = None
        self._storage_account = None
        self._restore_as_managed_vm = None
        self._instance_type = None
        self._encryption_key = None
        self._key_pair = None
        self._iam_role = None
        self._volume_type = None
        self._network_subnet = None
        self._security_group = None
        self.refresh()

    def _get_cleanroom_target_id(self):
        """Gets the target id associated with this target.

            Returns:
                str - id associated with this target

        """
        target = CleanroomTargets(self._commcell_object)
        return target.all_targets[self._cleanroom_target_name]

    def _delete_cleanroom_target(self):
        """Deletes the cleanroom target

            Raises:
                SDKException:
                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('DELETE', self._RECOVERY_TARGET_API)
        if flag:
            return flag
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))


    def _set_policy_type(self, policy_type):
        """Sets the policy type"""
        if policy_type == "AMAZON":
            self._policy_type = 1
        elif policy_type == "MICROSOFT":
            self._policy_type = 2
        elif policy_type == "AZURE_RESOURCE_MANAGER":
            self._policy_type = 7
        elif policy_type in ["VMW_BACKUP_LABTEMPLATE", "VMW_LIVEMOUNT"]:
            self._policy_type = 13
        else:
            self._policy_type = -1

    def _get_cleanroom_target_properties(self):
        """Gets the target properties of this target.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_TARGET_API)

        if flag:
            if response.json() and 'entity' in response.json():
                self._cleanroom_target_properties = response.json()
                self._application_type = self._cleanroom_target_properties['entity']['applicationType']
                self._destination_hypervisor = self._cleanroom_target_properties['entity']['destinationHypervisor'][
                    'name']
                self._vm_suffix = self._cleanroom_target_properties["vmDisplayName"].get("suffix", "")
                self._vm_prefix = self._cleanroom_target_properties["vmDisplayName"].get("prefix", "")
                access_node = self._cleanroom_target_properties.get("accessNode", {})
                node_type = access_node.get("type", "")

                self._access_node = (
                    "Automatic"
                    if node_type == "Automatic"
                    else {
                        "type": node_type,
                        "name": access_node.get("name", ""),
                        "id": access_node.get("id", "")
                    }
                    if node_type in ("Client", "Group")
                    else None
                )
                self._access_node_client_group = (self._cleanroom_target_properties.get('proxyClientGroupEntity', {})
                                                  .get('clientGroupName'))
                self._users = self._cleanroom_target_properties.get('securityOptions', {}).get('users', [])
                self._user_groups = self._cleanroom_target_properties.get('securityOptions', {}).get('userGroups', [])
                self._instance = self._cleanroom_target_properties["entity"].get("policyType", "")
                self._set_policy_type(self._instance)

                if self.policy_type == 1:
                    self._region = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                    .get('region', {})
                                    .get('name', ''))
                    self._availability_zone = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                               .get('availabilityZone', ''))
                    self._iam_role = (self._cleanroom_target_properties.get('amazonPolicy', {})
                                      .get('iamRole', {}).get('name', ''))
                    self._encryption_key = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                            .get('encryptionKey', {}).get('keyName', ''))
                    self._instance_type = (self._cleanroom_target_properties.get('amazonPolicy', {})
                                           .get('vmInstanceTypes', [{}])[0]
                                           .get('vmInstanceTypeName', ''))
                    self._security_group = (self._cleanroom_target_properties.get('securityOptions', {})
                                            .get('securityGroup', [{}])[0]
                                            .get('name', ''))
                    self._network_subnet = (self._cleanroom_target_properties.get('networkOptions', {})
                                            .get('network', ''))
                    self._volume_type = (self._cleanroom_target_properties.get('amazonPolicy', {})
                                         .get('volumeType', {}).get('name', ''))
                    self._key_pair = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                      .get('keyPair', ''))

                if self._policy_type == 7:
                    self._region = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                    .get('region', {})
                                    .get('name'))
                    self._availability_zone = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                               .get('availabilityZone'))
                    self._storage_account = (self._cleanroom_target_properties.get("destinationOptions", {})
                                             .get("dataStore", ""))

                    self._vm_size = (self._cleanroom_target_properties.get('amazonPolicy', {})
                                     .get('vmInstanceTypes', [{}])[0]
                                     .get('vmInstanceTypeName', ''))
                    self._disk_type = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                       .get('volumeType'))
                    self._virtual_network = (self._cleanroom_target_properties.get('networkOptions', {})
                                             .get('networkCard', {})
                                             .get('networkDisplayName'))
                    self._security_group = (self._cleanroom_target_properties.get('securityOptions', {})
                                            .get('securityGroups', [{}])[0]
                                            .get('name', ''))
                    self._create_public_ip = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                              .get('publicIP'))
                    self._restore_as_managed_vm = (self._cleanroom_target_properties.get('cloudDestinationOptions', {})
                                                   .get('restoreAsManagedVM'))
                    expiry_hours = (self._cleanroom_target_properties.get("liveMountOptions", {})
                                    .get("expirationTime", {})
                                    .get("minutesRetainUntil", ""))
                    expiry_days = (self._cleanroom_target_properties.get("liveMountOptions", {})
                                   .get("expirationTime", {})
                                   .get("daysRetainUntil", ""))
                    if expiry_hours:
                        self._expiration_time = f'{expiry_hours} hours'
                    elif expiry_days:
                        self._expiration_time = f'{expiry_days} days'
                    self._test_virtual_network = (self._cleanroom_target_properties.get('networkOptions', {})
                                                  .get('cloudNetwork', {})
                                                  .get('label'))
                    self._test_vm_size = (self._cleanroom_target_properties.get('amazonPolicy', {})
                                          .get('vmInstanceTypes', [{}])[0]
                                          .get('vmInstanceTypeName', ''))
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def cleanroom_target_id(self):
        """Returns: (str) the id of the cleanroom target"""
        return self._cleanroom_target_id

    @property
    def cleanroom_target_name(self):
        """Returns: (str) the display name of the cleanroom target"""
        return self._cleanroom_target_name

    @property
    def policy_type(self):
        """Returns: (str) the policy type ID
            1  - AWS
            2  - Microsoft Hyper-V
            7  - Azure
            13 - VMware
        """
        return self._policy_type

    @property
    def target_instance(self):
        return self._instance

    @property
    def application_type(self):
        """Returns: (str) the name of the application type
            0 - Replication type
            1 - Regular type
        """
        return self._application_type

    @property
    def destination_hypervisor(self):
        """Returns: (str) the client name of destination hypervisor"""
        return self._destination_hypervisor

    @property
    def access_node(self):
        """Returns: (str) the client name of the access node/proxy of the cleanroom target"""
        return self._access_node

    @property
    def access_node_client_group(self):
        """Returns: (str) The client group name set on the access node field of cleanroom target"""
        return self._access_node_client_group

    @property
    def security_user_names(self):
        """Returns: list<str> the names of the users who are used for ownership of the hypervisor and VMs"""
        return [user['userName'] for user in self._users]

    @property
    def vm_prefix(self):
        """Returns: (str) the prefix of the vm name to be prefixed to the destination VM"""
        return self._vm_prefix

    @property
    def vm_suffix(self):
        """Returns: (str) the suffix of the vm name to be suffixed to the destination VM"""
        return self._vm_suffix

    @property
    def expiration_time(self):
        """Returns: (str) VMware/Azure: the expiration time of the test boot VM/test failover VM
            eg: 4 hours or 3 days
        """
        return self._expiration_time

    @property
    def storage_account(self):
        """Returns: (str) Azure: the storage account name used to deploy the VM's storage"""
        return self._storage_account

    @property
    def region(self):
        """Return: (str) Azure: the cleanroom target region for destination VM"""
        return self._region

    @property
    def availability_zone(self):
        """Return: (str) Azure: the cleanroom target availability zone for destination VM"""
        return self._availability_zone

    @property
    def virtual_network(self):
        """Return: (str) Azure: the cleanroom target virtual network for destination VM"""
        return self._virtual_network

    @property
    def security_group(self):
        """Return: (str) Azure: the cleanroom target security group for destination VM"""
        return self._security_group

    @property
    def create_public_ip(self):
        """Return: (str) Azure: the cleanroom target create public group for destination VM"""
        return self._create_public_ip

    @property
    def vm_size(self):
        """Return: (str) Azure: the cleanroom target vm size for destination VM"""
        return self._vm_size

    @property
    def restore_as_managed_vm(self):
        """Returns: (bool) whether the destination VM will be a managed VM"""
        return self._restore_as_managed_vm

    @property
    def availability_zone(self):
        """Returns: (str) the availability zone of the cleanroom Recovery Group"""
        return self._availability_zone

    @property
    def iam_role(self):
        """Returns: (str) the IAM role name used for the cleanroom Recovery Group"""
        return self._iam_role

    @property
    def encryption_key(self):
        """Returns: (str) the encryption key name used for the cleanroom Recovery Group"""
        return self._encryption_key

    @property
    def instance_type(self):
        """Returns: (str) the instance type of the cleanroom Recovery Group"""
        return self._instance_type

    @property
    def volume_type(self):
        """Returns: (str) the volume type of the cleanroom Recovery Group"""
        return self._volume_type

    @property
    def network_subnet(self):
        """Returns: (str) the network subnet of the cleanroom Recovery Group"""
        return self._network_subnet

    @property
    def security_group(self):
        """Returns: (str) the security group of the cleanroom Recovery Group"""
        return self._security_group

    @property
    def key_pair(self):
        """Returns: (str) the key pair name used for the cleanroom Recovery Group"""
        return self._key_pair

    def refresh(self):
        """Refresh the properties of the cleanroom Target."""
        self._get_cleanroom_target_properties()

    def delete(self):
        """Deletes the Cleanroom Target. Returns: (bool) whether the target is deleted or not."""
        return self._delete_cleanroom_target()
