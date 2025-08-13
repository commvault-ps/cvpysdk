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

Runbook:   Class for creating a cleanroom recovery group and target using the new simplified runbook API

"""
from cvpysdk.exception import SDKException
from json.decoder import JSONDecodeError


class Runbook:
    """Class to perform actions on a cleanroom runbook"""

    def __init__(self, commcell_object):
        """Initialize the instance of the CleanroomRunbook class.

            Args:
                commcell_object   (object)    --  instance of the Commcell class

        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._recovery_group_id = None
        self._RUNBOOK_URL = commcell_object._services['CREATE_CLEANROOM_RUNBOOK']    

    def create(self, payload=dict()):
        """Creates a cleanroom runbook.

            Args:
                payload (dict)  --  payload for creating the runbook

            Returns:
                Response (dict) - response of the request
                    
                    {
                        "recoveryGroup": {
                            "id": 1234567890,
                            "name": "runbook_name"
                        }
                    }

            Raises:
                SDKException:
                    if payload is empty
                    if API response is empty
                    if API response is not success

        """
        if not payload:
            raise SDKException('RecoveryGroup', '101', 'Payload cannot be empty')
        flag, response = self._cvpysdk_object.make_request('POST', self._RUNBOOK_URL, payload=payload)
        
        if flag:
            try:
                response_json = response.json()
                if not response_json:
                    raise ValueError('Response', '102', 'Empty response received from the server')
                
                if "recoveryGroup" in response_json and "id" in response_json['recoveryGroup']:
                        self._recovery_group_id = response_json['recoveryGroup']['id']
                        return response_json
                else:
                    raise KeyError('Response', '102', 'Recovery group ID not found in the response')
            except JSONDecodeError:
                raise ValueError('Response', '102', 'Invalid response received from the server.')
        else:
            raise SDKException('Response', '101', self._commcell_object._update_response_(response.text))
            
    @property
    def recovery_group_id(self):
        """Returns recovery group id which gets initialized when runbook is created"""
        if self._recovery_group_id is not None:
            return int(self._recovery_group_id)
        return None

    def populate_payload(self, entities, target, region, node=None):
        """Builds the payload with the required fields for creating a runbook.

            Args:
                entities (dict)  --  entities payload to be populated
                target (dict)  --  target payload to be populated
                node (dict)  --  access node details to be populated
                                Optional when using existing target or existing hypervisor
                region (dict)  --  region details to be populated

            Returns:
                dict - populated payload

            Sample entities input format:
            entities= {
                    "name": "Runbook with existing target",
                    "entities": [
                        {
                            "instance_id": 1,
                            "instance_name": "DefaultInstanceName",
                            "client_id": 2,
                            "client_name": "devcs3",
                            "backupset_id": 3,
                            "backupset_name": "defaultBackupSet",
                            "subclient_id": 14,
                            "subclient_name": "small file",
                            "workload": "FILES",
                            "execution_order": 2
                        },
                        {
                            "instance_id": 6,
                            "instance_name": "Amazon Web Services",
                            "client_id": 10,
                            "client_name": "AWS",
                            "backupset_id": 14,
                            "backupset_name": "defaultBackupSet",
                            "vm_group_id": 18,
                            "vm_guid": "i-0d485455929da6c11",
                            "vm_name": "WindowsTestVM1",
                            "source_vendor": "AMAZON",
                            "workload": "VM",
                            "execution_order": 1
                        }
                    ]
                }
            If combining both VM and FILES workloads, the entities should be a list of dictionaries with the respective fields.

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
                    if entities input is empty
                    if invalid workload type is provided in payload
                    if target input is empty
        """
        if not isinstance(entities['name'], str):
            raise SDKException('RecoveryGroup', '101', 'Missing or invalid Runbook name')
        api_payload = {
                        "name": entities.get('name', 'cleanroom_runbook'),
                        "target": {
                            "options": {
                            "region": region if region else {},
                            "accessNode": {}
                            }
                        },
                        "entities": [
                        ],
                        "advancedOptions": {
                            "postRecoveryActions": [
                            {
                                "scriptCredentials": {},
                                "guestCredentials": {}
                            }
                            ],
                            "delayBetweenPriorityMachines": 0,
                            "continueOnFailure": False,
                            "recoveryExpirationOptions": {
                            "enableExpirationOption": True,
                            "daysToExpire": 7,
                            "isRescuedCommServe": True,
                            "expirationTime": 0
                            }
                        }
                    }

        #Populate the payload with list of entities
        if not entities or not entities.get('entities'):
            raise SDKException('RecoveryGroup', '101', 'Payload cannot be empty')
        else:
            for item in entities['entities']:
                workload = None
                if item['workload'] == 'VM':
                    workload = 8
                elif item['workload'] == 'FILES':
                    workload = 9
                else:
                    raise SDKException('RecoveryGroup', '101', 'Invalid workload type provided in payload')
                entity = {
                    "instance": {
                        "id": item.get('instance_id', 0),
                        "name": item.get("instance_name", "string")
                    },
                    "backupSet": {
                        "id": item.get('backupset_id', 0),
                        "name": item.get("backupset_name", "string")
                    },
                    "client": {
                        "id": item.get('hypervisor_id', 0) if item.get('hypervisor_id') else item.get('client_id', 0),
                        "name": item.get("hypervisor_name", "string") if item.get('hypervisor_name') else item.get('client_name', "string"),
                    },
                    "workload": workload,
                    "executionOrder": {
                        "priority": item.get('execution_order', 0)
                    },
                    "recoveryPointDetails": {
                        "inheritedFrom": "RECOVERY_GROUP",
                        "entityRecoveryPoint": 0,
                        "entityRecoveryPointCategory": "LATEST"
                    }              
                }
                if workload == 8:  # VM workload
                    vm_info = {
                        "vmGroup": {
                            "id": item.get("vm_group_id", 0)
                        },
                        "virtualMachine": {
                            "GUID": item.get("vm_guid", "<vm_guid>"),
                            "name": item.get("vm_name", "string")
                        },
                        "sourceVendor": item.get("source_vendor", "VMW")
                    }
                    entity.update(vm_info)
                elif workload == 9:  # FILES workload
                    file_info = {
                        "subclient": {
                            "id": item.get("subclient_id", 0),
                            "name": item.get("subclient_name", "string")
                        }
                    }
                    entity.update(file_info)
                api_payload['entities'].append(entity)
        #Populate the payload with target details
        #Populate the payload with access node details
        if node.get('access_node_id') is not None:  #Using existing access node or access node group
            access_node_entity = {
                "id": node.get('access_node_id', 0),
                "name": node.get('access_node_name', 'string'),
                "type": node.get('access_node_type', 3)
            }
            api_payload['target']['options']['accessNode'].update(access_node_entity)
        if not target:
            raise SDKException('RecoveryGroup', '101', 'Target payload cannot be empty')
        elif target.get('target_id') is not None and target.get('target_id') > 0 :  #Using existing target
            target_entity = {
                "entity": {
                "id": target.get('target_id', 0),
                "name": target.get('target_name', 'string')
                }
            }
            api_payload['target'].update(target_entity)
        else:
            options = {
                        "vendor": target.get('target_vendor', 'AZURE_V2')
                    }
            api_payload['target']['options'].update(options) 
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
                    api_payload['target']['options'].update(existing_hypervisor)
                    api_payload['target']['options']['accessNode'].update(access_node_entity)
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
                    api_payload['target']['options'].update(options)
        return api_payload