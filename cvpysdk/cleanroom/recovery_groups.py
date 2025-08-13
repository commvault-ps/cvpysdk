# -*- coding: utf-8 -*-
#
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
#
"""
Main file for performing Cleanroom recovery operations

RecoveryGroups:     Class for representing all the recovery groups

RecoveryGroup:      Class for a single recovery group selected, and to perform operations on that recovery group

"""
from enum import Enum

from cvpysdk.exception import SDKException
from json.decoder import JSONDecodeError

from cvpysdk.cleanroom.target import CleanroomTarget

from .recovery_entities import RecoveryEntities


class RecoveryGroups:
    """Class representing all the cleanroom recovery groups"""

    def __init__(self, commcell_object):
        """Initialize object of the RecoveryGroups class.

            Args:
                commcell_object (object)  --  instance of the Commcell class

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object

        self._RECOVERY_GROUPS_URL = commcell_object._services['ALL_RECOVERY_GROUPS']
        self._recovery_groups = None

        self.refresh()

    @property
    def all_groups(self):
        """Returns dict of all recovery groups.

         Returns dict    -   consists of all groups

                {
                     "group1_name": group1_id,
                     "group2_name": group2_id
                }

        """
        return self._recovery_groups

    def has_recovery_group(self, recovery_group_name):
        """Checks if a recovery group is present in the commcell.

            Args:
                recovery_group_name (str)  --  name of the recovery group

            Returns:
                bool - boolean output whether the group is present in commcell or not

            Raises:
                SDKException:
                    if type of the group name argument is not string

        """
        if not isinstance(recovery_group_name, str):
            raise SDKException('RecoveryGroup', '101')

        return self._recovery_groups and recovery_group_name in self._recovery_groups

    def get(self, recovery_group_name):
        """Returns a recovery group object.

            Args:
                recovery_group_name (str)  --  name of the recovery group

            Returns:
                object - instance of the recovery group class for the given group name

            Raises:
                SDKException:
                    if type of the group name argument is not string

                    if no group exists with the given name

        """
        if not isinstance(recovery_group_name, str):
            raise SDKException('RecoveryGroup', '101')
        else:
            if self.has_recovery_group(recovery_group_name):
                return RecoveryGroup(
                    self._commcell_object,
                    recovery_group_name,
                    self.all_groups[recovery_group_name]
                )

            raise SDKException('RecoveryGroup', '102',
                               'No recovery group exists with name: {0}'.format(recovery_group_name))

    def refresh(self):
        """Refresh the recovery groups"""
        self._recovery_groups = self._get_recovery_groups()

    def __str__(self):
        """Representation string consisting of all recovery groups .

            Returns:
                str     -   string of all the groups

        """
        representation_string = '{:^5}\t{:^20}\n\n'.format('S. No.', 'RecoveryGroup')

        for index, group in enumerate(self._recovery_groups):
            sub_str = '{:^5}\t{:20}\n'.format(
                index + 1,
                group
            )
            representation_string += sub_str

        return representation_string.strip()

    def _get_recovery_groups(self):
        """Gets all the recovery groups.

            Returns:
                dict - consists of all recovery groups in the client
                    {
                         "group1_name": group1_id,
                         "group2_name": group2_id
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_GROUPS_URL)

        if flag:
            try:
                json_resp = response.json()

                group_name_id_dict = {group['name']: group['id'] for group in json_resp['recoveryGroups']}

                return group_name_id_dict
            except (JSONDecodeError, KeyError):
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))


class RecoveryStatus(Enum):
    NO_STATUS = 0
    NONE = 0
    NOT_READY = 1
    READY = 2
    RECOVERED = 3
    FAILED = 4
    RECOVERED_WITH_ERRORS = 5
    IN_PROGRESS = 6
    CLEANED_UP = 7
    MARK_AS_FAILED = 8
    CLEANUP_FAILED = 9

class RecoveryStatusNotReadyCategory(Enum):
    NONE = 0
    INVALID_VM_NAME = 1
    INVALID_COPY = 2
    MARK_AS_FAILED = 4
    V1_INDEXING_NOT_SUPPORTED = 16
    INVALID_SMART_FOLDER = 8
    LAST_BACKUP_OUTDATED = 32
    LAST_BACKUP_NOT_READY = 64
    MANAGED_IDENTITY_ENABLED = 128
    AUTOSCALING_DISABLED = 256

class RecoveryGroup:
    """Class to perform actions on a recovery group"""

    def __init__(self, commcell_object, recovery_group_name, recovery_group_id=None):
        """Initialize the instance of the RecoveryGroup class.

            Args:
                commcell_object   (object)    --  instance of the Commcell class

                recovery_group_name      (str)       --  name of the target

                recovery_group_id        (str)       --  id of the target (default: None)

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self.recovery_group_name = recovery_group_name
        if recovery_group_id is not None:
            self._recovery_group_id = str(recovery_group_id)
        else:
            # get id from RecoveryGroups class
            self._recovery_group_id = RecoveryGroups(commcell_object).all_groups[recovery_group_name]
        self._RECOVERY_GROUP_URL = commcell_object._services['RECOVERY_GROUP'] % self._recovery_group_id
        self._RECOVER_URL = commcell_object._services['RECOVERY_GROUP_RECOVER'] % self._recovery_group_id
        self._RECOVERY_GROUP_THREATS_COUNT = commcell_object._services['RECOVERY_GROUP_THREATS_COUNT'] % self._recovery_group_id

        # will be set when refresh is called
        self._properties = None
        self.refresh()
        self._recovery_entities = RecoveryEntities(self, self._commcell_object)
        self._recovery_target = CleanroomTarget(self._commcell_object, self.target_name)

    @property
    def recovery_entities(self):
        """Returns RecoveryEntity Manager object using which RecoveryEnity object can be created further"""
        return self._recovery_entities

    @property
    def id(self):
        """recovery group id"""
        return int(self._recovery_group_id)

    @property
    def name(self):
        return self.recovery_group_name

    @property
    def target_name(self):
        return self.entities[0]['target']['name']

    @property
    def entities(self):
        """All entities properties in recovery group"""
        return self._properties['entities']

    @property
    def entities_list(self):
        """List if all the entities in a recovery group"""
        entity_list = []
        for entity in self.entities:
            entity_list.append(entity['name'])
        return entity_list

    @property
    def entities_id(self):
        """List of entities' id in the recovery group"""
        entity_list_id = []
        for entity in self.entities:
            entity_list_id.append(entity['id'])
        return entity_list_id

    @property
    def security_group(self):
        """Returns: (str) Azure: the security group name"""
        return self.entities[0]['recoveryConfiguration']['configuration']['azure']['overrideReplicationOptions']['securityGroup']['id']

    @property
    def virtual_network(self):
        """Returns: (str) Azure: the virtual network name"""
        return self.entities[0]['recoveryConfiguration']['configuration']['azure']['overrideReplicationOptions'][
            'virtualNetwork']['networkName']

    @property
    def resource_group(self):
        """Returns: (str) Azure: the resource group name"""
        return self.entities[0]['recoveryConfiguration']['configuration']['azure']['resourceGroup']

    @property
    def storage_account(self):
        """Returns: (str) Azure: the storage account name used to deploy the VM's storage"""
        return self.entities[0]['recoveryConfiguration']['configuration']['azure']['storageAccount']

    @property
    def get_new_target_name(self):
        """Returns the created target name for the recovery group created via custom config"""
        return f'{self.recovery_group_name}-Target'

    @property
    def get_new_hypervisor_name(self):
        """Returns the created hypervisor name for the recovery group created via custom config"""
        return f'{self.get_new_target_name}-Hypervisor'

    @property
    def is_threatscan_enabled(self):
        """Returns boolean value of threat scan property set at recovery group level"""
        return self._properties['recoveryGroup']['threatScan']['enableThreatScan']

    @property
    def is_windefender_enabled(self):
        """Returns boolean value of windows defender property set at recovery group level"""
        return self._properties['recoveryGroup']['threatScan']['enableWindowsDefenderScan']

    def _recover_entities(self, entity_ids, threat_scan=False, win_defender_scan=False):
        """
        Sends request to recover all entities with specified ids

        Args:
            entity_ids         (list)    --  iterable of entity ids
            threat_scan       (bool)    --  run security scan on restored VM
                                            default: False
            win_defender_scan (bool)    --  run security scan on restored VM
                                            default: False

        Returns:
            job_id: job id of recovery

        Raises:
            SDKException:
                if response is empty

                if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('POST', self._RECOVER_URL, payload={
            'recoveryGroup': {
                'id': self.id
            },
            'entities': [{'id': e_id} for e_id in entity_ids],
            'threatScan': {
                'enableThreatScan': threat_scan if not self.is_threatscan_enabled else self.is_threatscan_enabled,
                'enableWindowsDefenderScan': win_defender_scan if not self.is_windefender_enabled else self.is_windefender_enabled
            }
        })

        if flag:
            try:
                return response.json()['jobId']
            except (JSONDecodeError, KeyError):
                raise SDKException('Response', '102', 'Job id not found in response')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def get_threats_count(self):
        """
        Sends request to get overall threats count of recovery group

        Returns:
            (int) threatCount: threats count of recovery group

        Raises:
            SDKException:
                if response is empty

                if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_GROUP_THREATS_COUNT)

        if flag:
            try:
                return response.json()['KPI'][0]["threatCount"]
            except (JSONDecodeError, KeyError):
                raise SDKException('Response', '102', 'Threat count not found in response')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def recover_all(self,threat_scan=False, win_defender_scan=False):
        """
        Sends request to recover all entities

        Returns:
            job_id: job id of recovery

        Raises:
            SDKException:
            if response is empty

            if response is not success

        """
        eligible_entities = [entity['id'] for entity in self.entities if
                             entity['recoveryStatus'] not in [RecoveryStatus.NOT_READY.value,
                                                              RecoveryStatus.IN_PROGRESS.value] and
                     (not win_defender_scan or (win_defender_scan and entity['osType'] == 0))]

        return self._recover_entities(eligible_entities, threat_scan, win_defender_scan)

    def refresh(self):
        """Refresh the recovery group"""
        self._properties = self._get_recovery_group_properties()

    def _get_recovery_group_properties(self):
        """Gets recovery group properties.

            Returns:
                dict - properties for the recovey group

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_GROUP_URL)

        if flag:
            try:
                return response.json()
            except JSONDecodeError:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def delete(self):
        """
        Sends a request to delete a replication Group

        Raises:
            SDKException:
                if response is empty

                if response is not success
        """

        flag, response = self._cvpysdk_object.make_request('DELETE', self._RECOVERY_GROUP_URL)

        if flag:
            try:
                return response.json()
            except JSONDecodeError:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    def get_entity_status(self):
        """
        Returns the recovery status and readiness category for entities.

        Returns:
            dict: A mapping of entity names to their recovery status and not-ready category.
        """
        status_map = {}
        for entity in self.entities:
            if 'name' not in entity:
                continue  # Skip entities without a name

            status_map[entity['name']] = {
                'recoveryStatus': entity.get('recoveryStatus', None),
                'recoveryStatusNotReadyCategory': entity.get('recoveryStatusNotReadyCategory', None)
            }
        return status_map

    def validate_new_recovery_target_exists(self):
        """Verifies if the created new recovery target via custom config exists with correct name."""
        observed_target = self.target_name
        expected_target = self.get_new_target_name

        return observed_target == expected_target

    def validate_new_hypervisor_exists(self):
        """Verifies if the created new hypervisor via custom config exists with correct name."""
        observed_hypervisor = self._recovery_target.destination_hypervisor
        expected_hypervisor = self.get_new_hypervisor_name

        return observed_hypervisor == expected_hypervisor

