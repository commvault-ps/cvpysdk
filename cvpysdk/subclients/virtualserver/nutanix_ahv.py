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

"""File for operating on a Virtual Server Nutanix AHV Subclient.

nutanixsubclient is the only class defined in this file.

nutanixsubclient: Derived class from VirtualServerSubClient  Base class, representing a
                           nutanix AHV Subclient, and to perform operations on that Subclient

nutanixsubclient:

    full_vm_restore_out_of_place()                  --  restores the VM  specified in
                                                        to the specified client, at the
                                                        specified destination location

    full_vm_restore_in_place()                      --  restores the VM specified by the
                                                        user to the same location
"""


from ..vssubclient import VirtualServerSubclient
from ...exception import SDKException


class nutanixsubclient(VirtualServerSubclient):
    """Derived class from VirtualServerSubclient  Base class, representing a
    nutanix  virtual server subclient,and to perform operations on that subclient."""

    def __init__(self, backupset_object, subclient_name, subclient_id=None):
        """Initialize the Instance object for the given Virtual Server instance.
        Args
        class_object (backupset_object, subclient_name, subclient_id)  --  instance of the
                                         backupset class, subclient name, subclient id

        """
        self.diskExtension = ["none"]
        super(nutanixsubclient, self).__init__(
            backupset_object, subclient_name, subclient_id)

    def full_vm_restore_out_of_place(self,
                                     vm_to_restore=None,
                                     host=None,
                                     container=None,
                                     proxy_client=None,
                                     restore_new_name=None,
                                     overwrite=True,
                                     power_on=True,
                                     copy_precedence=0,
                                     restore_option=None,
                                     vcenter_client=None,
                                     run_security_scan=False,
                                     **kwargs):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
                    at the specified destination location.

            Args:

                vm_to_restore         (list)       --  provide the VM name to restore

                host                  (str)        -- ESX host for Vm to restore

                container             (str)        -- provide the storage account to restore

                proxy_client          (str)        -- provide the proxy client to restore

                restore_new_name      (str)        -- provide the new restore name

                overwrite               (bool)       --  overwrite the existing VM
                                                        default: True

                power_on                (bool)       --  power on the  restored VM
                                                        default: True

                copy_precedence       (int)         --  copy precedence value
                                                        default: 0

                restore_option        (dict)       --  complete dictionary with
                                                       all advanced option

                vcenter_client        (str)        --  name of the vcenter client where the VM
                                                        should be restored
                                                        default: {}

                run_security_scan       (bool)       -- run threat analysis on VM
                                                        default:False

                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_out_of_place
                    eg:
                    v2_details          (dict)       -- details for v2 subclient
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if destination_path is not a string

                    if failed to initialize job

                    if response is empty

                    if response is not success
                """
        # restore options
        if restore_option is None:
            restore_option = {}
        restore_option["v2_details"] = kwargs.get("v2_details", None)

        # check input parameters are correct
        if bool(restore_option):
            if not (isinstance(overwrite, bool) and
                    isinstance(power_on, bool)):
                raise SDKException('Subclient', '101')

        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            esx_host=host,
            esx_server=vcenter_client,
            vcenter_client=vcenter_client,
            datastore=container,
            client_name=proxy_client,
            in_place=False,
            restore_new_name=restore_new_name,
            run_security_scan=run_security_scan,
        )

        # set attr for all the option in restore xml from user inputs

        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_restore_in_place(self,
                                 vm_to_restore=None,
                                 overwrite=True,
                                 power_on=True,
                                 copy_precedence=0,
                                 **kwargs):
        """Restores the FULL Virtual machine specified  in the input  list to the client,
            to the location same as source .

            Args:
                vm_to_restore          (list)      --  provide the VM name to restore

                overwrite               (bool)      --  overwrite the existing VM
                                                        default: True

                power_on                (bool)      --  power on the  restored VM
                                                        default: True

                copy_precedence        (int)       -- storage policy copy precedence
                                                      from which browse has to be performed

                **kwargs                         : Arbitrary keyword arguments Properties as of
                                                     full_vm_restore_in_place
                    eg:
                    v2_details          (dict)       -- details for v2 subclient
                                                    eg: check clients.vmclient.VMClient._child_job_subclient_details


            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:

                    if failed to initialize job

                    if response is empty

                    if response is not success
        """
        restore_option = {"v2_details": kwargs.get("v2_details", None)}
        # check mandatory input parameters are correct
        if not (isinstance(overwrite, bool) and
                isinstance(power_on, bool)):
            raise SDKException('Subclient', '101')
        # set attr for all the option in restore xml from user inputs
        self._set_restore_inputs(
            restore_option,
            vm_to_restore=self._set_vm_to_restore(vm_to_restore),
            unconditional_overwrite=overwrite,
            power_on=power_on,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            in_place=True
        )
        request_json = self._prepare_fullvm_restore_json(restore_option)
        return self._process_restore_response(request_json)

    def full_vm_conversion_vmware(
            self,
            vcenter_client,
            destination_os_name,
            vm_to_restore=None,
            esx_host=None,
            datastore=None,
            overwrite=True,
            power_on=True,
            copy_precedence=0,
            disk_option='Original',
            transport_mode='Auto',
            proxy_client=None,
            destination_network=None
        ):
        """
        Conversion from AHV VM to VMware
        Args:
                vcenter_client    (str) -- name of the vcenter client
                                                  where the VM should be
                                                    restored.

                destination_os_name      (base string)- os of source VM

                vm_to_restore          (dict)  --  dict containing the VM name(s) to restore as
                                                   keys and the new VM name(s) as their values.
                                                   Input empty string for default VM name for
                                                   restored VM.
                                                    default: {}

                esx_host          (str) -- destination esx host
                                                    restores to the source VM
                                                    esx if this value is not
                                                    specified

                datastore         (str) -- datastore where the
                                                  restored VM should be located
                                                  restores to the source VM
                                                  datastore if this value is
                                                  not specified

                overwrite         (bool)       -- overwrite the existing VM
                                                  default: True

                power_on          (bool)       -- power on the  restored VM
                                                  default: True

                copy_precedence   (int)        -- copy precedence value
                                                  default: 0

                disk_option       (str) -- disk provisioning for the
                                                  restored vm
                                                  Options for input are: 'Original',
                                                  'Thick Lazy Zero', 'Thin', 'Thick Eager Zero'
                                                  default: Original

                transport_mode    (str) -- transport mode to be used for
                                                  the restore.
                                                  Options for input are: 'Auto', 'SAN', 'Hot Add',
                                                  'NBD', 'NBD SSL'
                                                  default: Auto

                proxy_client      (str) -- destination proxy client

                destination_network (str)-- destiantion network
                                                    to which VM has to be connected

            Returns:
                object - instance of the Job class for this restore job

            Raises:
                SDKException:
                    if inputs are not of correct type as per definition

                    if failed to initialize job

                    if response is empty

                    if response is not success

        """

        restore_option = {}

        subclient = self._set_vm_conversion_defaults(vcenter_client, restore_option)
        instance = subclient._backupset_object._instance_object
        disk_option_value = subclient._disk_option[disk_option]
        transport_mode_value = subclient._transport_mode[transport_mode]
        esx_server = instance.server_host_name[0]

        #setting restore vms
        vm_list = None
        if vm_to_restore:
            vm_list = list(vm_to_restore.keys())

        self._set_restore_inputs(
            restore_option,
            in_place=False,
            vcenter_client=vcenter_client,
            datastore=datastore,
            esx_host=esx_host,
            esx_server=esx_server,
            unconditional_overwrite=overwrite,
            client_name=proxy_client,
            power_on=power_on,
            vm_to_restore=self._set_vm_to_restore(vm_list),
            disk_option=disk_option_value,
            transport_mode=transport_mode_value,
            copy_precedence=copy_precedence,
            volume_level_restore=1,
            destination_instance=instance.instance_name,
            backupset_client_name=instance._agent_object._client_object.client_name,
            destination_network=destination_network,
            destination_os_name=destination_os_name
        )

        request_json = self._prepare_fullvm_restore_json(restore_option)
        disk_options = request_json['taskInfo']['subTasks'][0]['options']['restoreOptions']['virtualServerRstOption'][
            'diskLevelVMRestoreOption']
        for disk_info in disk_options['advancedRestoreOptions'][0]['disks']:
            disk_info['newName'] = ''

        return self._process_restore_response(request_json)

    def attach_disk_restore(
        self,
        vm_name,
        host=None,
        host_user=None,
        host_pass=None,
        container=None,
        proxy_client=None,
        copy_precedence=0,
        disk_uuids=None,
        destination_vm=None,
        destination_vm_guid=None):
        """Attach restored disks from a protected VM to a destination AHV VM.
            - Browse available VMs and their associated disks
            - Attach one or more disks from backup to a specified target VM
        Args:
            vm_name (str): Name of the protected VM
            host (str): AHV host name.
            host_user (str): AHV host username.
            host_pass (str): AHV host password.
            container (str): AHV storage container where disks will be restord
            proxy_client (str): Destination proxy client to use.
            copy_precedence (int): Storage policy copy precedence for the restore.
            disk_uuids (list): Specific disk names to attach.
            destination_vm (str): Destination VM name 
            destination_vm_guid (str): Destination VM GUID/UUID 
        Returns:
            Job: Instance of the Job class representing the running restore job.
        Raises:
            SDKException: If inputs are invalid, browse fails, or the restore
                submission fails.
        """
        # Resolve VM ids/names from browse
        vm_names, vm_ids = self._get_vm_ids_and_names_dict_from_browse()
        _attach_disk_restore_option = {}
    
        # Normalize / validate inputs (mirror OpenStack implementation style)
        if disk_uuids is None:
            disk_uuids = []
    
        if copy_precedence:
            _attach_disk_restore_option['copy_precedence_applicable'] = True
    
        # Fetch all disks available for the source VM
        if vm_name not in vm_ids:
            available_vms = list(vm_ids.keys())
            raise SDKException(
                'Subclient',
                '101',
                (f"VM '{vm_name}' was not found. "
                 f"Available VMs: {available_vms}"))
    
        disk_list, disk_info_dict = self.disk_level_browse(f"\\{vm_ids[vm_name]}")
    
        # If no disk list provided, attach all; else validate requested names exist
        if not disk_uuids:
            for each_disk_path in disk_list:
                disk_uuids.append(each_disk_path.split('\\')[-1])
        else:
            for each_disk in disk_uuids:
                expected_path = f"\\{vm_name}\\{each_disk}"
                if expected_path not in disk_list:
                    available_disks = [p.split('\\')[-1] for p in disk_list]
                    raise SDKException(
                        'Subclient',
                        '111',
                        (f"Disk '{each_disk}' was not found for VM '{vm_name}'. "
                         f"Available disks: {available_disks}"))
        # Choose proxy client
        if proxy_client is not None:
            _attach_disk_restore_option['client'] = proxy_client
        else:
            _attach_disk_restore_option['client'] = (
                self._backupset_object._instance_object.co_ordinator
            )
    
        # Build source item list for the disks
        src_item_list = []
        for each_disk in disk_uuids:
            disk_name = each_disk.split("\\")[-1]
            src_item_list.append(f"\\{vm_ids[vm_name]}\\{disk_name}")
        # Set options required by the attach-disk workflow
        _attach_disk_restore_option['paths'] = src_item_list
        _attach_disk_restore_option['newName'] = destination_vm
        _attach_disk_restore_option['newGUID'] = destination_vm_guid
        _attach_disk_restore_option['userName'] = host_user
        _attach_disk_restore_option['password'] = host_pass
    
        self._set_restore_inputs(
            _attach_disk_restore_option,
            in_place=False,
            copy_precedence=copy_precedence,
            vm_to_restore=vm_name,
            esxHost=host,
            datastore=container,
            paths=src_item_list,
            volume_level_restore=6
        )
        # Prepare and submit the attach-disk restore
        request_json = self._prepare_attach_disk_restore_json(
            _attach_disk_restore_option
        )
        return self._process_restore_response(request_json)

