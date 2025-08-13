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

"""Main file for getting Recovery job details and phases

RecoveryJob: Class for representing all the Recovery jobs

RecoveryJob(Job):
    __init__(commcell_object,
            job_id)                 -- Initialise object of RecoveryJob
    _get_recovery_job_stats()       -- Gets the Recovery job statistics
    get_phases()                    -- Gets the phases of the Recovery job
"""

import time
from cvpysdk.job import Job
from cvpysdk.exception import SDKException
from cvpysdk.drorchestration.dr_orchestration_job_phase import DRJobPhases, DRJobPhaseToText



class RecoveryJob(Job):
    """Class for performing Recovery Job operation"""

    def __init__(self, commcell_object, job_id):
        """Initialise the Recovery job"""
        self._recovery_job_stats = None

        service_url = commcell_object._services['DRORCHESTRATION_JOB_STATS']
        self._RECOVERY_STATS = service_url % job_id

        Job.__init__(self, commcell_object, job_id)

    def __repr__(self):
        representation_string = 'RecoveryJob class instance for job id: "{0}"'
        return representation_string.format(self.job_id)

    def _get_recovery_job_stats(self):
        """Gets the statistics for the Recovery Job
        Returns:
                [{
                    'jobId': 123,
                    'recoveryEntityId': 1
                    'replicationId': 1,
                    'phase': [{
                            'phase': 1,
                            'status': 0,
                            'startTime': {
                                '_type_': 0,
                                'time': 0
                            },
                            'endTime': {
                                '_type_': 0,
                                'time': 0
                            },
                            'entity': {
                                'clientName': 'vm1'
                            },
                            'phaseInfo': {
                                'job': [
                                    {
                                        'jobid': 123,
                                        'opType': 1,
                                        'failure': {
                                            'errorMessage': 'Error message'
                                        },
                                        'entity': {
                                            'clientName': 'vm1',
                                            '_type_': 0
                                        }
                                    }
                                ]
                            }
                        }]
                    'client': {
                        'clientId': 0,
                        'clientName': 'vm1'
                    },
                    'vapp': {
                        'vAppId': 1
                    }
                }]
        """
        flag, response = self._commcell_object._cvpysdk_object.make_request(
            'GET', self._RECOVERY_STATS)

        if flag:
            if response.json() and 'job' in response.json():
                return response.json()['job'] or []
            elif response.json() and 'errors' in response.json():
                errors = response.json().get('errors', [{}])
                error_list = errors[0].get('errList', [{}])
                error_code = error_list[0].get('errorCode', 0)
                error_message = error_list.get('errLogMessage', '').strip()
                if error_code != 0:
                    response_string = self._commcell_object._update_response_(
                        error_message)
                    raise SDKException('Response', '101', response_string)
            else:
                if response.json():
                    raise SDKException('Response', '102')
        else:
            response_string = self._commcell_object._update_response_(
                response.text)
            raise SDKException('Response', '101', response_string)

    def _initialize_job_properties(self):
        """Initialises the job properties and then initialises the Recovery job details"""
        Job._initialize_job_properties(self)
        self._recovery_job_stats = self._get_recovery_job_stats()

    def get_phases(self):
        """
        Gets the phases of the recovery job
        Returns: dictionaries of phases for each source and destination VM pair
            {"source_vm_1": [{
                'phase_name': enum - Enum of phase short name and full name mapping,
                'phase_status': int - 0 for success, 1 for failed,
                'start_time': int - timestamp of start of job,
                'end_time': int - timestamp of end of job,
                'machine_name': str - The name of the machine Job is executing on,
                'error_message': str - Error message, if any,
            }],
            }
        """
        job_stats = {}
        if not self._recovery_job_stats:
            return job_stats
        for pair_stats in self._recovery_job_stats:
            phases = []
            for phase in pair_stats.get('phase', []):
                phases.append({
                    # We use common enum for job phases
                    'phase_name': DRJobPhaseToText[DRJobPhases(phase.get('phase', '')).name]
                    if phase.get('phase', '') else '',
                    'phase_status': phase.get('status', 1),
                    'start_time': phase.get('startTime', {}).get('time', ''),
                    'end_time': phase.get('endTime', {}).get('time', ''),
                    'machine_name': phase.get('entity', {}).get('clientName', ''),
                    'error_message': phase.get('phaseInfo', {}).get('job', [{}])[0].get('failure', {})
                                     .get('errorMessage', ''),
                    'job_id': str(phase.get('phaseInfo', {}).get('job', [{}])[0].get('jobid', '')),
                })
            job_stats[str(pair_stats.get('client', {}).get('clientName', ''))] = phases
        return job_stats

    def get_restore_vm_from_recovery_job(self, entity, max_retries=30, check_frequency=10):
        """
        Retrieves the restore job ID for a specific VM entity during a recovery job.

        Retries for up to `max_retries` times, checking every `check_frequency` seconds.

        Args:
            entity (str): Name of the VM entity.
            max_retries (int): Number of attempts to check for the restore phase.
            check_frequency (int): Time in seconds between attempts.

        Returns:
            int: Job ID of the restore VM job.

        Raises:
            Exception: If the RESTORE_VM phase is not found after retries.
        """
        for attempt in range(max_retries):
            recovery_job_obj = RecoveryJob(self._commcell_object, self.job_id)
            phases = recovery_job_obj.get_phases().get(entity, [])

            for phase in phases:
                if phase.get('phase_name').name == "RESTORE_VM":
                    restore_job_id = phase.get('job_id')
                    return restore_job_id

            time.sleep(check_frequency)

        raise Exception(f"Failed to locate RESTORE_VM phase for VM '{entity}' in job {self.job_id}")
