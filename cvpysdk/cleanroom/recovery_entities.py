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

from cvpysdk.exception import SDKException
from enum import Enum
from json.decoder import JSONDecodeError
from cvpysdk.cleanroom.recoveryjob import RecoveryJob


WORKLOADS = {
    0: "GENERIC",
    1: "O365",
    2: "SALESFORCE",
    3: "EXCHANGE",
    4: "SHAREPOINT",
    5: "ONEDRIVE",
    6: "TEAMS",
    7: "DYNAMICS_365",
    8: "VIRTUAL SERVER",
    9: "FILE SYSTEM"
}

INSTANCES = {
    'AZURE_V2': 'Azure Resource Manager',
    'AMAZON': 'Amazon Web Services'
}

RecoveryDestinationVendor = {
    7 : 'azure',
    4 : 'amazon'
}

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
    RECOVERED_WITH_THREATS = 10

class RecoveryReadiness(Enum):
    NO_STATUS = 0
    NONE = 0
    NOT_READY = 1
    READY = 2

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

class ValidationStatus(Enum):
    NONE = 0
    IN_PROGRESS = 1
    SUCCESS = 2
    FAILED = 3
    WARNING = 4

class RecoveryEntities:

    def __init__(self, recovery_group, commcell_object):
        """This acts as a Recovery Entity manager, which will help creating recovery entity object"""
        self._recovery_group_object = recovery_group # gets the recovery group object
        self._commcell_object = commcell_object # gets commcell object

    def get(self, entity_id):
        """Returns Recovery entity object for the provided entity id which is unique

             Args:
                 entity_id (int)  --  id of recovery entity

             Returns:
                 object -- instance of recovery entity for the given entity id

             Raises:
                 SDKException:
                     if recoverygroup does not exist with that name

                     if recovery entity does not exists with that id

         """
        entity_id = int(entity_id)
        if self._recovery_group_object.recovery_group_name:
            if self.entity_exists(entity_id):
                return RecoveryEntity(self._commcell_object, self._recovery_group_object,
                                      entity_id)
            raise SDKException('RecoveryEnity', '102',
                               'No recovery entity exists with id: {0}'.format(entity_id))
        raise SDKException('RecoveryGroup', '102',
                               'Recovery group name is empty: {0}'.format(self._recovery_group_object.recovery_group_name))


    def entity_exists(self, entity_id):
        for entity in self._recovery_group_object.entities:
            if entity['id'] == entity_id:
                return True
        return False

class RecoveryEntity:
    """Class to perform actions on a recovery entity"""

    def __init__(self, commcell_object, recovery_group_object, recovery_entity_id):
        """Initialize the instance of the RecoveryEntity class.

            Args:
                commcell_object   (object)    --  instance of the Commcell class

                recovery_entity_id (int) -- entity id

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._recovery_group =recovery_group_object
        self._recovery_target = self._commcell_object.cleanroom_targets.get(self._recovery_group.target_name)
        self._recovery_entity_id = recovery_entity_id

        self._source_vm = None
        self._destination_vm = None
        self._last_recovery_job = None
        self._last_restore_job = None
        self._parent = None
        self._recovery_readiness_status = None
        self._recovery_status = None
        self._validation_status = None
        self._validation_results = None
        self._recovery_point = None
        self._workload = None
        self._source_client_object = None
        self._source_agent_object = None
        self._source_instance_object = None
        self._source_subclient_object = None
        self._destination_client_object = None
        self._destination_agent_object = None
        self._destination_instance_object = None

        self._recovery_config_dict = None

        self._properties = None

        self._RECOVERY_ENTITY_URL = commcell_object._services['RECOVERY_ENTITY'] % self._recovery_entity_id
        self.refresh()


    def _get_entity_recovery_options(self):

        """Gets recovery entity recovery options

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request('GET', self._RECOVERY_ENTITY_URL)

        if flag:
            try:
                # Attempt to decode the JSON response
                response_data = response.json()

                if not response_data:
                    raise SDKException('Response', '102', 'Response contains no data.')

                # If data is present, process the response
                self._properties = response_data
                self._source_vm = self._properties['name']
                self._destination_vm = self._properties['destinationName']
                self._parent = self._properties.get('vmGroup', '')
                self._destination_proxy_client_object = 'Automatic' if self._recovery_target.access_node == 'Automatic' else self._commcell_object.clients.get(
                self._recovery_target.access_node['name']) if self._recovery_target.access_node[
                                                                      'type'] == 'Client' else None

                if self._properties['recoveryStatusNotReadyCategory'] != 0:
                    """In this case readiness status is Not Ready"""
                    self._recovery_readiness_status = RecoveryStatusNotReadyCategory(self._properties['recoveryStatusNotReadyCategory']).name
                else:
                    self._recovery_readiness_status = RecoveryReadiness.READY.name
                self._last_recovery_job = self._properties['lastRecoveryJobId']
                if self._last_recovery_job != 0:
                    recovery_job = RecoveryJob(self._commcell_object, self._last_recovery_job)
                    phases = recovery_job.get_phases().get(self._source_vm, [])
                    for phase in phases:
                        if phase.get('phase_name').name == 'RESTORE_VM' and phase.get('job_id'):
                            self._last_restore_job = phase.get('job_id')
                self._recovery_status = RecoveryStatus(self._properties['recoveryStatus']).name
                self._validation_status = ValidationStatus(self._properties['validationStatus']).name
                # validation results are available for only threat scan/windows defender enabled recovery jobs
                if 'validationResults' in self._properties.keys():
                    validation_results = self._properties.get('validationResults', {})
                    self._validation_results = {
                        'output': validation_results[0].get('output'),
                        'failureReason': validation_results[0].get('failureReason'),
                        'name': validation_results[0].get('name'),
                        'validationStatus':validation_results[0].get('validationStatus'),
                        'threatInfo': validation_results[0].get('threatInfo')
                    }
                else:
                    pass
                recovery_point_details = self._properties.get('recoveryPointDetails', {})
                self._recovery_point = {
                        'entityRecoveryPointCategory': recovery_point_details.get('entityRecoveryPointCategory'),
                        'entityRecoveryPoint': recovery_point_details.get('entityRecoveryPoint'),
                        'inheritedFrom': recovery_point_details.get('inheritedFrom')
                    }
                self._workload = WORKLOADS[self._properties['workload']]
                self._source_client = self._properties['client']['name']
                self._source_agent = WORKLOADS[self._properties['workload']]
                self._source_instance = self._properties['instance']['name']
                self._source_subclient = self._properties['vmGroup']['name']
                self._destination_client = self._recovery_target.destination_hypervisor
                self._destination_agent = WORKLOADS[self._properties['workload']]
                self._destination_instance = INSTANCES[self._recovery_target.target_instance]
                """Returns a dict of all entities restore options"""
                self._recovery_config_dict = {
                     self._properties['name']: self._properties['recoveryConfiguration']['configuration'][RecoveryDestinationVendor[self._recovery_target.policy_type]]
                }

            except JSONDecodeError:
                raise SDKException('Response', '101', 'Failed to decode JSON from the response.')
            except KeyError as e:
                raise SDKException('Response', '101', f'Missing expected key in the response: {str(e)}')

        # If the request was unsuccessful, raise an exception
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))

    @property
    def commcell(self):
        """Returns commcell object"""
        return self._commcell_object

    @property
    def entity_id(self):
        """Returns entity id"""
        return self._recovery_entity_id

    @property
    def source_vm(self):
        """Returns source entity name"""
        return self._source_vm

    @property
    def destination_vm(self):
        """Returns destination enetity name"""
        return self._destination_vm

    @property
    def recovery_group_name(self):
        """Returns name of the recovery group with which this entity is associated"""
        return self._recovery_group.recovery_group_name

    @property
    def recovery_target_name(self):
        """Returns the name of the recovery target with which this entity is associated"""
        return self._recovery_target.cleanroom_target_name

    @property
    def entity_readiness_status(self):
        """Returns the readiness state of the entity"""
        return self._recovery_readiness_status

    @property
    def entity_recovery_status(self):
        """Returns the recovery status of the entity"""
        return self._recovery_status

    @property
    def validation_status(self):
        """Returns the validation status of the entity"""
        return self._validation_status

    @property
    def validation_results(self):
        """Returns the validation results of the entity"""
        return self._validation_results

    @property
    def recoveryPointDetails(self):
        """Returns dictionary of recovery point details"""
        return self._recovery_point

    @property
    def lastRecoveryJob(self):
        """Returns last recovery job"""
        return self._last_recovery_job

    @property
    def lastRestoreJob(self):
        """Returns last restore job"""
        return self._last_restore_job

    @property
    def parent(self):
        """Returns the vm group of the source entity"""
        return self._parent

    @property
    def workload(self):
        """Returns the workload of the source entity"""
        return self._workload

    def all_properties(self):
        """Returns all the properties of an entity"""
        return self._properties

    @property
    def recovery_config_dict(self):
        """Returns dict of recovery options per entity"""
        return self._recovery_config_dict

    @property
    def check_entity_id(self):
        """Returns boolean if recovery group exists and it has the entity"""
        if self._recovery_group.recovery_group_name is not None:
            if self._properties['id'] == self._recovery_entity_id:
                return True
            else:
                return False

    @property
    def source_client(self):
        """Returns entity source client object Hypervisor Client"""
        return self._source_client

    @property
    def source_agent(self):
        """Returns entity source agent Workloads - VM/Files"""
        return self._source_agent

    @property
    def source_instance(self):
        """Returns entity source instance- Azure/AWS.."""
        return self._source_instance

    @property
    def source_subclient(self):
        """Returns entity subclient """
        return self._source_subclient

    @property
    def destination_client(self):
        """Returns entity destination client Hypervisor Client"""
        return self._destination_client

    @property
    def destination_agent(self):
        """Returns entity destination agent Workloads - VM/Files"""
        return self._destination_agent

    @property
    def destination_instance(self):
        """Returns entity destination instance - Azure/AWS.."""
        return self._destination_instance

    def refresh(self):
        """Refreshes the properties of the live sync"""
        self._get_entity_recovery_options()
