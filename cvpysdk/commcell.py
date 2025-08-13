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
"""Main file for performing operations on Commcell via REST API.

Commcell is the main class for the CVPySDK python package.

Commcell:   Initializes a connection to the commcell and is a wrapper for the entire commcell ops.

Commcell:
    __init__()                  --  initialize instance of the Commcell class

    __repr__()                  --  return the name of the commcell, user is connected to,
    along with the user name of the connected user

    __enter__()                 --  returns the current instance, using the "with" context manager

    __exit__()                  --  logs out the user associated with the current instance

    _update_response_()         --  returns only the relevant response for the response received
    from the server

    _remove_attribs_()          --  removes all the attributs associated with the commcell
    object upon call to the logout method

    _get_commserv_details()     --  gets the details of the commserv, the Commcell class instance
    is initialized for

    _qoperation_execute()       --  runs the qoperation execute rest api on specified input xml

    _qoperation_execscript()    --  runs the qoperation execute qscript with specified arguements

    get_gxglobalparam_value()	--	makes a rest api call to get values from GXGlobalParam

    _set_gxglobalparam_value    --  updates GXGlobalParam(commcell level configuration parameters)

    verify_owner_assignment_config()    -- verifies that the ownership assignments settings are configured
    and set properly

    logout()                    --  logs out the user associated with the current instance

    request()                   --  runs an input HTTP request on the API specified,
    and returns its response

    send_mail()                 --  sends an email to the specified user

    refresh()                   --  refresh the properties associated with the Commcell
    class instance
    run_data_aging()            --  triggers data aging job from the commcell level

    get_saml_token()            --  returns the SAML token for the currently logged-in user

    add_additional_setting()    --  adds registry key to the commserve property

    delete_additional_setting() --  deletes registry key from the commserve property

    get_configured_additional_setting() --  To get configured additional settings from the commserve property

    download_software()         --  triggers the Download Software job with the given options

    copy_software()             --  triggers the Copy Software job with the given options

    sync_remote_cache()         --  syncs remote cache

    get_remote_cache()     		--  returns the instance of the RemoteCache class

    push_servicepack_and_hotfixes() --  triggers installation of service pack and hotfixes

    install_software()              --  triggers the install Software job with the given options

    remote_cache_clients()      --  fetches the list of Remote Cache configured for a particular Admin/Tenant

    enable_auth_code()              --  executes the request on the server to enable Auth Code
    for installation on the commcell

    disable_auth_code()             --  disables auth code requirement for installation on the commcell

    enable_shared_laptop()          --   Executes the request on the server to enable Shared Laptop on commcell

    disable_shared_laptop()         --  Executes the request on the server to disable Shared Laptop on commcell

    execute_qcommand()              --  executes the ExecuteQCommand API on the commcell

    add_associations_to_saml_app()  --  Adds the given user under associations of the SAML app

    register_commcell()             -- registers a commcell

    is_commcell_registered()       -- checks if the commcell is registered

    get_default_plan()                  -- Get the default plans associed with the commcell

    get_security_associations()         -- Get the security associations associated with the commcell

    get_password_encryption_config()    -- Get the Password encryption configuration for the commcell

    get_email_settings()                -- Get the SMTP settings for the commcell

    set_email_settings()                -- Set the SMTP settings for the commcell

    get_commcell_properties()           -- Get the general, privacy and other properties of commcell

    get_commcell_organization_properties()     -- Get the organization properties of commcell

    enable_tfa()                           --   Enables two factor authentication on this commcell

    disable_tfa()                          --  Disables two factor authentication on this commcell

    _get_commserv_metadata()               -- Returns back the commserv metadata on this commcell

    _get_commserv_oem_id()               -- Returns back the commserv OEM ID on this commcell

    enable_privacy()                    --  Enables users to enable data privacy on commcell

    disable_privacy()                   --  Enables users to disable data privacy on commcell

    switch_to_company()         --  Login to company as an operator, just like using switcher on Command Center

    reset_company()             --  Switch back to Commcell

    switch_to_global()          --  Adds comet fanout headers, like global mode in multi commcell command center

    is_global_scope()           --  Check if comet headers are active

    reset_to_local()            --  Removes comet headers, like switching back to local commcell

    allow_users_to_enable_passkey()     --      Enable or Disable passkey authorization for company administrators and client owners

    passkey()                       --  Updates Passkey properties of the commcell

    get_sla_configuration()         --  gets the sla configuration details at commcell level

    get_workload_region()           --  gets the current workload region

    set_workload_region()           --  sets the workload region at commcell level

    get_user_suggestions()          --  gets details of entities matching given term

    enable_limit_user_logon_attempts()  --  Enables limit user logon attempts feature.

    disable_limit_user_logon_attempts()   -- Disables limit user logon attempts feature.


Commcell instance Attributes
============================

    **commserv_guid**           --  returns the `CommServ` GUID, class instance is initalized for

    **commserv_hostname**       --  returns the hostname of the `CommServ`, class instance is
    initalized for

    **commserv_name**           --  returns the `CommServ` name, class instance is initalized for

    **commserv_timezone**       --  returns the time zone of the `CommServ`,
    class instance is initalized for

    **commserv_timezone_name**  --  returns the name of the `CommServ` time zone,
    class instance is initalized for

    **commserv_version**        --  returns the ContentStore version installed on the `CommServ`,
    class instance is initalized for

    **version**                 --  returns the complete version info of the commserv

    **release_name**            --  returns the release name of this commserv

    **commcell_id**             --  returns the `CommCell` ID

    **commserv_metadata**       -- returns the commserv metadata of the commserv

    **commserv_oem_id**         -- returns the commserv OEM ID of the commserv

    **webconsole_hostname**     --  returns the host name of the `webconsole`,
    class instance is connected to

    **auth_token**              --  returns the `Authtoken` for the current session to the commcell

    **commcell_username**       --  returns the associated `user` name for the current session
    to the commcell

    **device_id**               --  returns the id associated with the calling machine

    *name_change*               --  returns the name change object of the commcell

    **clients**                 --  returns the instance of the `Clients` class,
    to interact with the clients added on the Commcell

    **commserv_cache**          --  returns the instance of the `CommServeCache` class

    **media_agents**            --  returns the instance of the `MediaAgents` class,
    to interact with the media agents associated with the Commcell class instance

    **workflows**               --  returns the instance of the `WorkFlow` class,
    to interact with the workflows deployed on the Commcell

    **alerts**                  --  returns the instance of the `Alerts` class,
    to interact with the alerts available on the Commcell

    **disk_libraries**          --  returns the instance of the `DiskLibraries` class,
    to interact with the disk libraries added on the Commcell

    **tape_libraries**          --  returns the instance of the `TapeLibraries` class,
    to interact with the tape libraries added on the Commcell
    
    **storage_policies**        --  returns the instance of the `StoragePolicies` class,
    to interact with the storage policies available on the Commcell

    **schedule_policies**       --  returns the instance of the `SchedulePolicies` class,
    to interact with the schedule policies added to the Commcell

    **schedules**       --  returns the instance of the `Schedules` class,
    to interact with the schedules associated to the Commcell

    **user_groups**             --  returns the instance of the `UserGroups` class,
    to interact with the user groups added to the Commcell

    **domains**                 --  returns the instance of the `Domains` class,
    to interact with the domains added to the Commcell

    **client_groups**           --  returns the instance of the `ClientGroups` class,
    to interact with the client groups added to the Commcell

    **global_filters**          --  returns the instance of the `GlobalFilters` class,
    to interact with the global filters available on the Commcell

    **datacube**                --  returns the instance of the `Datacube` class,
    to interact with the datacube engine deployed on the Commcell

    **content_analyzers**       --  returns the instance of the `ContentAnalyzers` class,
    to interact with the CA cloud deployed on the Commcell

    **activate**                --  returns the instance of the `Activate` class,
    to interact with activate apps on the Commcell

    **threat_indicators**       --  returns the instance of Servers class, to interact with threat indicators on the commcell

    **export_sets**             --  returns the instance of the `ExportSets` class
    to interact with compliance search export sets on the Commcell

    **plans**                   --  returns the instance of the `Plans` class,
    to interact with the plans associated with the Commcell

    **job_controller**          --  returns the instance of the `JobController` class,
    to interact with all the jobs finished / running on the Commcell

    **users**                   --  returns the instance of the `Users` class,
    to interact with the users added to the Commcell

    **roles**                   --  returns the instance of the `Roles` class,
    to interact with the roles added to the Commcell

    **credentials**             --  returns the instance of the `Credentials` class,
    to interact with the credentials records added to the Commcell

    **download_center**         --  returns the instance of the `DownloadCenter` class,
    to interact with the download center repositories deployed on the Commcell WebConsole

    **organizations**           --  returns the instance of the `Organizations` class,
    to interact with the organizations/companies added on the Commcell

    **storage_pools**           --  returns the instance of the `StoragePools` class,
    to interact with the storage pools added to the Commcell Admin Console

    **monitoring_policies**     --  returns the instance of the `MonitoringPolicies` class,
    to interact with the MonitoringPolicies added to the Commcell

    **operation_window**        -- returns the instance of the 'OperationWindow' class,
    to interact with the opeartion windows of commcell

    **array_management**        --  returns the instance of the `ArrayManagement` class,
    to perform SNAP related operations on the Commcell

    **activity_control**        --  returns the instance of the `ActivityControl` class,
    to interact with the Activity Control on the Commcell

    **event_viewer**            --  returns the instance of the `Events` class,
    to interact with the Events associated on the Commcell

    **disasterrecovery**    -- returns the instance of the 'DisasterRecovery' class,
    to run disaster recovery backup , restore operations.

    **commserv_client**         --  returns the client object associated with the
    commserver

    **identity_management**     --  returns the instance of the 'IdentityManagementApps
    class to perform identity management operations on the commcell class

    **system**                  --  returns the instance of the 'System' class to perform
    system related operations on the commcell

    **commcell_migration**      --  returns the instance of the 'CommCellMigration' class,
    to interact with the Commcell Export & Import on the Commcell

    **grc**      --  returns the instance of the 'GlobalRepositoryCell' class,
    to interact with the registered commcells and setup/modify GRC schedules

    **service_commcells**       --  returns the instance of the `ServiceCommcells` class, to
    perform service commcell related operations

    **backup_network_pairs**    --  returns the instance of 'BackupNetworkPairs' class to
    perform backup network pairs operations on the commcell class

    **recovery_targets**        -- Returns the instance of RecoverTargets class

    **cleanroom_targets**       -- -- Returns the instance of CleanroomTargets class

    **reports**                 --  Return the instance of Report class

    **job_management**          --  Returns an instance of the JobManagement class.

    **hac_clusters**            --  Returns an instance of the HAC Clusters class

    **network_topologies**      --  Returns an instance of NetworkTopologies class

    **index_pools**             --  Returns an instance of the IndexPools class

    **deduplications_engines    --  Returnes the instance of the DeduplicationEngines class
    to interact wtih deduplication enines available on the commcell

    **two_factor_authentication**   --  Returns an instance of the TwoFactorAuthentication class.

    **is_tfa_enabled**              --  Returns the status of tfa on this commcell.

    **tfa_enabled_user_groups**     -- Returns user group names on which tfa is enabled.
    only for user group inclusion tfa.

    **tags                          -- Returns the instance of entity tags class

    **is_linux_commserv**           -- boolean specifying if CommServer is installed on linux cs.

    **default_timezone**            -- Default timezone used by all the operations performed via cvpysdk.

    **metallic**                 -- Returns the instance of CVMetallic class

    **key_management_servers**      -- Returns the instance of `KeyManagementServers` class

    **is_passkey_enabled**          -- Returns True if Passkey is enabled on commcell

    **databases**                    -- Returns the list of databases on the commcell

    **database_instances**           -- Returns the list of database instances on the commcell

    **database_instant_clones**      -- Returns the list of database instant clone jobs active on the commcell

    **cost_assessment**             -- Returns the instance of the CostAssessment class

"""

from __future__ import absolute_import
from __future__ import unicode_literals

import getpass
import socket
from contextlib import contextmanager

import xmltodict

from base64 import b64encode

from requests.exceptions import SSLError
from requests.exceptions import Timeout

# ConnectionError is a built-in exception, do not override it
from requests.exceptions import ConnectionError as RequestsConnectionError

from .activate import Activate
from .activateapps.compliance_utils import ExportSets
from .constants import UserRole
from .activateapps.tco import CostAssessment
from .services import get_services
from .cvpysdk import CVPySDK
from .client import Clients
from .monitoringapps.threat_indicators import TAServers
from .alert import Alerts
from .snmp_configs import SNMPConfigurations
from .storage import MediaAgents
from .storage import DiskLibraries
from .storage import TapeLibraries
from .security.usergroup import UserGroups, UserGroup
from .domains import Domains, Domain
from .tags import Tags
from .workflow import WorkFlows
from .exception import SDKException
from .clientgroup import ClientGroups
from .globalfilter import GlobalFilters
from .datacube.datacube import Datacube
from .content_analyzer import ContentAnalyzers
from .network_topology import NetworkTopologies
from .plan import Plans
from .job import JobController
from .security.user import Users, User
from .security.role import Roles
from .security.two_factor_authentication import TwoFactorAuthentication
from .credential_manager import Credentials
from .download_center import DownloadCenter
from .resource_pool import ResourcePools
from .organization import Organizations, Organization
from .storage_pool import StoragePools
from .monitoring import MonitoringPolicies
from .policy import Policies
from .schedules import SchedulePattern
from .schedules import Schedules
from .activitycontrol import ActivityControl
from .eventviewer import Events
from .array_management import ArrayManagement
from .disasterrecovery import DisasterRecovery
from .operation_window import OperationWindow
from .identity_management import IdentityManagementApps
from .system import System
from .commcell_migration import CommCellMigration, GlobalRepositoryCell
from .deployment.download import Download
from .deployment.cache_config import CommServeCache
from .deployment.cache_config import RemoteCache
from .deployment.install import Install
from .name_change import NameChange
from .backup_network_pairs import BackupNetworkPairs
from .reports import report
from .recovery_targets import RecoveryTargets
from .cleanroom.target import CleanroomTargets
from .cleanroom.recovery_groups import RecoveryGroups
from .drorchestration.replication_groups import ReplicationGroups
from .drorchestration.failovergroups import FailoverGroups
from .drorchestration.blr_pairs import BLRPairs
from .job import JobManagement
from .index_server import IndexServers
from .hac_clusters import HACClusters
from .index_pools import IndexPools
from .deduplication_engines import DeduplicationEngines
from .metallic import Metallic
from .key_management_server import KeyManagementServers
from .regions import Regions
from .service_commcells import ServiceCommcells
from urllib.parse import urlparse

USER_LOGGED_OUT_MESSAGE = 'User Logged Out. Please initialize the Commcell object again.'
USER_DOES_NOT_HAVE_PERMISSION = "User does not have permission on commcell properties"
"""str:     Message to be returned to the user, when trying the get the value of an attribute
of the Commcell class, after the user was logged out.

"""


class Commcell(object):
    """Class for establishing a session to the Commcell via Commvault REST API."""

    def __init__(
            self,
            webconsole_hostname,
            commcell_username=None,
            commcell_password=None,
            authtoken=None,
            force_https=False,
            certificate_path=None,
            is_service_commcell=None,
            verify_ssl = True,
            **kwargs):
        """Initialize the Commcell object with the values required for doing the API operations.

            Commcell Username and Password can be None, if QSDK / SAML token is being given
            as the input by the user.

            If both the Commcell Password and the Authtoken are None,
            then the user will be prompted to enter the password via command line.


            Args:
                webconsole_hostname     (str)   --  webconsole host Name / IP address

                    e.g.:

                        -   webclient.company.com

                        -   xxx.xxx.xxx.xxx


                commcell_username       (str)   --  username for log in to the commcell console

                    default: None


                commcell_password       (str)   --  plain-text password for log in to the console

                    default: None


                authtoken               (str)   --  QSDK / SAML token for log in to the console

                    default: None

                verify_ssl               (str)   --  Pass this choose to verify SSL requests to commcell

                    default: True

            **Note** : If SAML token is to be used to login to service commcell please set is_service_commcell=True


                force_https             (bool)  --  boolean flag to specify whether to force the
                connection to the commcell only via HTTPS

                if the flag is set to **False**, SDK first tries to connect to the commcell via
                HTTPS, but if that fails, it tries to connect via HTTP

                if flag is set to **True**, it'll only try via HTTPS, and exit if it fails

                    default: False


                certificate_path        (str)   --  path of the CA_BUNDLE or directory with
                certificates of trusted CAs (including trusted self-signed certificates)

                    default: None

            **Note** If certificate path is provided, force_https is set to True

                is_service_commcell     (bool) --  True if login into service (child commcell)
                                                   False if it is a normal login

                    default: None

            **Note** In case of Multicommcell Login, if we wanted to login into child commcell (Service commcell)
                        set is_service_commcell to True
                
                **kwargs:
                    web_service_url      (str)   --  url of webservice for the api requests

                    user_agent           (str)   --  user agent header to set for the requests

                    master_commcell  (Commcell)  --  instance of the master commcell's object

                    master_hostname       (str)  --  hostname of the master commcell where to authenticate
                                                     if master_commcell object is not provided

            Returns:
                object  -   instance of this class

            Raises:
                SDKException:
                    if the web service is down or not reachable

                    if no token is received upon log in

        """
        web_service_url = kwargs.get("web_service_url", None)
        web_service = []
        
        if certificate_path:
            force_https = True
            
        if not web_service_url:
            web_service = [
				r'https://{0}/commandcenter/api/'.format(webconsole_hostname)
			]

            if force_https is False:
                web_service.append(r'http://{0}/commandcenter/api/'.format(webconsole_hostname))
        else:
            web_service = []
            if web_service_url.startswith("https://") or web_service_url.startswith("http://"):
                web_service.append(r'{0}/'.format(web_service_url))
            else:
                web_service.append(r'https://{0}/'.format(web_service_url))
                if force_https is False:
                    web_service.append(r'http://{0}/'.format(web_service_url))
                

        self._user = commcell_username

        self._password = None

        self._user_agent = kwargs.get('user_agent')

        self._headers = {
            'Host': webconsole_hostname,
            'Accept': 'application/json',
            'Content-type': 'application/json',
            'Authtoken': None
        }
        if self._user_agent:
            self._headers['User-Agent'] = self._user_agent
        
        if web_service_url:
            parsed_web_service_url = urlparse(web_service_url)
            self._headers['Host'] = f"{parsed_web_service_url.netloc}"

        self._device_id = socket.getfqdn()

        if idp_hostname := kwargs.get("master_hostname"):
            self._master_commcell = Commcell(
                idp_hostname, commcell_username, commcell_password, authtoken,
                force_https, certificate_path, False, verify_ssl
            )
        else:
            self._master_commcell = kwargs.get("master_commcell")

        if self._master_commcell:
            is_service_commcell = True
            authtoken = self._master_commcell.get_saml_token()

        self._is_service_commcell = is_service_commcell

        # Checks if the service is running or not
        for service in web_service:
            self._web_service = service
            try:
                if service.startswith("http:"):
                    # if force_https is false and if verify_ssl is true, we still allow HTTP calls to be made.
                    # since verify_ssl is set, the calls for http is failing. Below change allow http calls to be made
                    verify_ssl = False
                    self._cvpysdk_object = CVPySDK(self, certificate_path, verify_ssl)
                else:
                    self._cvpysdk_object = CVPySDK(self, certificate_path, verify_ssl)
                if self._cvpysdk_object._is_valid_service():
                    break
            except (RequestsConnectionError, SSLError, Timeout):
                if force_https:
                    raise
        else:
            raise SDKException('Commcell', '101', f'[{webconsole_hostname}]')

        # Initialize all the services with this commcell service
        self._services = get_services(self._web_service)

        validity_err = None
        self._is_saml_login = False

        if isinstance(commcell_password, dict):
            authtoken = commcell_password['Authtoken']

        if authtoken and not is_service_commcell:
            if authtoken.startswith('QSDK ') or authtoken.startswith('SAML ') or authtoken.startswith('Bearer '):
                self._headers['Authtoken'] = authtoken
            else:
                self._headers['Authtoken'] = '{0}{1}'.format('QSDK ', authtoken)

            try:
                self._is_saml_login = True if authtoken.startswith('SAML ') else False
                self._user = self._cvpysdk_object.who_am_i()
            except SDKException as error:
                self._headers['Authtoken'] = None
                validity_err = error

        if not self._headers['Authtoken'] and commcell_username is not None:
            if commcell_password is None:
                commcell_password = getpass.getpass('Please enter the Commcell Password: ')

            self._password = b64encode(commcell_password.encode()).decode()
            # Login to the commcell with the credentials provided
            # and store the token in the headers
            self._headers['Authtoken'] = self._cvpysdk_object._login()

        if self.is_service_commcell and authtoken is not None and authtoken.startswith('SAML '):
            self._master_saml_token = authtoken
            self._headers['Authtoken'] = self._cvpysdk_object._login()
            self._user = self._cvpysdk_object.who_am_i()
        if not self._headers['Authtoken']:
            if isinstance(validity_err, Exception):
                raise validity_err

            raise SDKException('Commcell', '102')

        self._master_saml_token = None
        self._commserv_name = None
        self._commserv_hostname = None
        self._commserv_timezone = None
        self._commserv_timezone_name = None
        self._commserv_guid = None
        self._commserv_version = None
        self._version_info = None
        self._release_name = None
        self._is_linux_commserv = None
        self._commserv_metadata = None
        self._commserv_oem_id = None
        self._user_mappings = None
        self._user_role = None
        self._user_org = None

        self._id = None
        self._clients = None
        self._commserv_cache = None
        self._remote_cache = None
        self._media_agents = None
        self._workflows = None
        self._disaster_recovery = None
        self._alerts = None
        self._disk_libraries = None
        self._tape_libraries = None
        self._storage_policies = None
        self._schedule_policies = None
        self._schedules = None
        self._policies = None
        self._user_groups = None
        self._domains = None
        self._client_groups = None
        self._global_filters = None
        self._datacube = None
        self._activate = None
        self._export_sets = None
        self._content_analyzers = None
        self._resource_pool = None
        self._plans = None
        self._job_controller = None
        self._users = None
        self._roles = None
        self._credentials = None
        self._download_center = None
        self._organizations = None
        self._storage_pools = None
        self._activity_control = None
        self._events = None
        self._monitoring_policies = None
        self._array_management = None
        self._operation_window = None
        self._commserv_client = None
        self._identity_management = None
        self._system = None
        self._commcell_migration = None
        self._grc = None
        self._registered_commcells = None
        self._backup_network_pairs = None
        self._reports = None
        self._replication_groups = None
        self._failover_groups = None
        self._recovery_targets = None
        self._recovery_groups = None
        self._cleanroom_targets = None
        self._threat_indicators = None
        self._blr_pairs = None
        self._job_management = None
        self._index_servers = None
        self._hac_clusters = None
        self._nw_topo = None
        self._index_pools = None
        self._deduplication_engines = None
        self._tfa = None
        self._metallic = None
        self._kms = None
        self._privacy = None
        self._commcell_properties = None
        self._regions = None
        self._snmp_configurations = None
        self._tags = None
        self._additional_settings = None
        self._service_commcells = None
        self._databases = None
        self._database_instances = None
        self._database_instant_clones = None
        self._cost_assessment = None
        self._commserv_details_loaded = False
        self._commserv_details_set = False
        self.refresh()

        del self._password

    def __repr__(self):
        """String representation of the instance of this class.

            Returns:
                str - string about the details of the Commcell class instance

        """
        rep =  (f'Commcell class instance '
                f'of Commcell: [{self.webconsole_hostname}] '
                f'for User: [{self.commcell_username}]')
        if self.is_global_scope():
            rep += ' in Global Scope'
        if self.operating_company:
            rep += f' operating on Company: [{self.operating_company}]'
        return rep

    def __enter__(self):
        """Returns the current instance.

            Returns:
                object  -   the initialized instance referred by self

        """
        return self

    def __exit__(self, exception_type, exception_value, traceback):
        """Logs out the user associated with the current instance."""
        output = self._cvpysdk_object._logout()
        self._remove_attribs_()
        return output

    def _update_response_(self, input_string):
        """Returns only the relevant response from the response received from the server.

            Args:
                input_string    (str)   --  input string to retrieve the relevant response from

            Returns:
                str     -   final response to be used

        """
        if '<title>' in input_string and '</title>' in input_string:
            response_string = input_string.split("<title>")[1]
            response_string = response_string.split("</title>")[0]
            return response_string

        return input_string

    def _remove_attribs_(self):
        """Removes all the attributes associated with the instance of this class."""
        del self._clients
        del self._commserv_cache
        del self._remote_cache
        del self._media_agents
        del self._workflows
        del self._alerts
        del self._disk_libraries
        del self._tape_libraries
        del self._storage_policies
        del self._schedule_policies
        del self._schedules
        del self._user_groups
        del self._policies
        del self._domains
        del self._roles
        del self._credentials
        del self._client_groups
        del self._global_filters
        del self._datacube
        del self._activate
        del self._content_analyzers
        del self._resource_pool
        del self._plans
        del self._job_controller
        del self._users
        del self._download_center
        del self._organizations
        del self._storage_pools
        del self._recovery_targets
        del self._cleanroom_targets
        del self._threat_indicators
        del self._replication_groups
        del self._blr_pairs
        del self._activity_control
        del self._events
        del self._monitoring_policies
        del self._array_management
        del self._operation_window
        del self._commserv_client
        del self._identity_management
        del self._system
        del self._web_service
        del self._cvpysdk_object
        del self._device_id
        del self._services
        del self._disaster_recovery
        del self._commcell_migration
        del self._grc
        del self._backup_network_pairs
        del self._job_management
        del self._index_servers
        del self._hac_clusters
        del self._nw_topo
        del self._index_pools
        del self._deduplication_engines
        del self._is_service_commcell
        del self._master_saml_token
        del self._tfa
        del self._metallic
        del self._kms
        del self._tags
        del self

    def _set_commserv_details(self, commcell_info):
        """Sets the CommServ details for the Commcell class instance.

            Args:
                commcell_info    (object)    --  commcell information object

            Returns:
                None

        """
        self._commserv_guid = commcell_info.commserv_guid
        self._commserv_hostname = commcell_info.commserv_hostname
        self._commserv_name = commcell_info.commserv_name
        self._commserv_timezone = commcell_info.commserv_timezone
        self._commserv_timezone_name = commcell_info.commserv_timezone_name
        self._commserv_version = commcell_info.commserv_version
        self._version_info = commcell_info.version
        self._id = commcell_info.commserv_id
        self._release_name = commcell_info.release_name
        self._commserv_details_loaded = True
        self._commserv_details_set = True

    def _get_commserv_details(self):
        """Gets the details of the CommServ, the Commcell class instance is initialized for,
            and updates the class instance attributes.

            Returns:
                None

            Raises:
                SDKException:
                    if failed to get commserv details

                    if response received is empty

                    if response is not success

        """
        import re

        flag, response = self._cvpysdk_object.make_request('GET', self._services['COMMSERV'])

        if flag:
            if response.json():
                try:
                    self._commserv_guid = response.json()['commcell'].get('csGUID')
                    self._commserv_hostname = response.json()['hostName']
                    self._commserv_name = response.json()['commcell']['commCellName']
                    self._commserv_timezone_name = response.json()['csTimeZone']['TimeZoneName']
                    self._commserv_version = response.json()['currentSPVersion']
                    version_info = response.json().get('csVersionInfo')
                    self._id = response.json()['commcell']['commCellId']
                    self._release_name = response.json().get('releaseName')

                    try:
                        self._commserv_timezone = re.search(
                            r'\(.*', response.json()['timeZone']
                        ).group()
                    except:
                        # in case where timezone string might be missing strings like
                        # (UTC+5:30) substitute the prepending strings like 0:-300: with ''
                        self._commserv_timezone = re.sub(
                            r'^([+|-]*\d*:)*', '', response.json()['timeZone']
                        )

                    # set commcell version (E.g. 11.21.0)
                    version_replace_strings = {
                        '.0 SP': '.',
                        ' SP': '.',
                        ' HPK': '.',
                        '+': '',
                        '-': '',
                        'a': '.1',
                        'b': '.2'
                    }

                    for key, value in version_replace_strings.items():
                        version_info = version_info.replace(key, value)

                    self._version_info = version_info + '.0' * (3 - len(version_info.split('.')))
                    self._commserv_details_loaded = True

                except KeyError as error:
                    raise SDKException('Commcell', '103', 'Key does not exist: {0}'.format(error))
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text) + 
                               ". You may need to provide View Commcell permission to the logged-in user. ")

    def _qoperation_execute(self, request_xml, return_xml=False):
        """Makes a qoperation execute rest api call

            Args:
                request_xml     (str)   --  request xml that is to be passed
                return_xml      (bool)  --  if True, will return xml response instead of json

            Returns:
                dict    -   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        accept_type_initial = self._headers['Accept']
        if return_xml:
            self._headers['Accept'] = 'application/xml'

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QCOMMAND'], request_xml
        )

        if flag:
            if response.ok:
                try:
                    if return_xml:
                        self._headers['Accept'] = accept_type_initial # reset initial accept type
                        return response.text
                    return response.json()
                except ValueError:
                    return {'output': response}
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def qoperation_execute(self, request_xml, **kwargs):
        """Wrapper for def _qoperation_execute(self, request_xml)

            Args:
                request_xml     (str)   --  request xml that is to be passed
                **kwargs:
                    return_xml  (bool)  --  if True, will get the xml response instead of json

            Returns:
                dict    -   JSON response received from the server.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success
        """

        return self._qoperation_execute(request_xml, **kwargs)

    @staticmethod
    def _convert_days_to_epoch(days):
        """
        convert the days to epoch time stamp
        Args:
            days: Number of days to convert

        Returns:
            from_time : days - now  . start time in unix format
            to_time   : now . end time in unix format
        """
        import datetime
        import time
        now = datetime.datetime.now()
        then = now - datetime.timedelta(days=days)
        start_dt = int(time.mktime(then.timetuple()))
        end_dt = int(time.mktime(now.timetuple()))
        return start_dt, end_dt

    @property
    def commcell_id(self):
        """Returns the ID of the CommCell."""
        if self._id is None:
            self._get_commserv_details()
        return self._id

    def _qoperation_execscript(self, arguments):
        """Makes a qoperation execute qscript with specified arguements

            Args:
                arguments     (str)   --  arguements that is to be passed

            Returns:
                dict    -   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXECUTE_QSCRIPT'] % arguments)

        if flag:
            if response.ok:
                try:
                    return response.json()
                except ValueError:
                    return {'output': response.text}
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_gxglobalparam_value(self, parameters):
        """Makes a rest api call to get values from GXGlobalParam

            Args:
                parameters      (str/list)  --  The single parameter name or list of parameter names to get value for

            Returns:
                str     --      If parameters argument is a string. None if the parameter is not found in response

                list    --      If parameters argument is a list.

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """

        parameters_orig = parameters
        if isinstance(parameters, str):
            parameters = [parameters]

        if not isinstance(parameters, list):
            raise SDKException('Commcell', '107')

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['GET_GLOBAL_PARAM'], {
                'globalParamsRequestList': parameters
            }
        )

        if flag:
            if response.json():
                param_results = response.json().get('globalParamsResultList')

                # If requested parameter is a string, then return the single value directly instead of the list response
                if isinstance(parameters_orig, str):
                    for param_result in param_results:
                        if param_result.get('name').lower() == parameters_orig.lower():
                            return param_result.get('value')

                    # Return None if the requested parameter is not found in the response
                    return None

                return param_results
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _set_gxglobalparam_value(self, request_json):
        """ Updates GXGlobalParam table (Commcell level configuration parameters)

            Args:
                request_json (dict)   --  request json that is to be passed

                    Sample: {
                                "name": "",
                                "value": ""
                            }
                OR
                request_json (list)   --  list of Global Param settings
                    Sample: [
                                {
                                    "name": "",
                                    "value": ""
                                },
                                ...
                            ]

            Returns:
                dict                --   json response received from the server

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        if isinstance(request_json, list):
            global_params_list = request_json
            payload = {
                "App_SetGlobalParamsReq": {
                    "globalParams": global_params_list
                }
            }
            return self.qoperation_execute(payload)

        if not isinstance(request_json, dict):
            message = f"Received: {type(request_json)}. Expected: dict, list"
            raise SDKException('Commcell', 107, message)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['SET_GLOBAL_PARAM'], request_json
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def verify_owner_assignment_config(self):

        """ Verifies that the ownership assignments settings are configured and set properly

        Returns:
                dict    -   json response received from the server

        Raises:
            SDKException:
                if response is empty

                if response is not success

                if ownership assignment is not correct

        """
        flag, response = self._cvpysdk_object.make_request(
            "GET", self._services["SET_COMMCELL_PROPERTIES"]
        )

        if flag:
            try:
                return response.json()
            except ValueError:
                return {'output': response}
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def commserv_guid(self):
        """Returns the GUID of the CommServ."""
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_guid

    @property
    def commserv_hostname(self):
        """Returns the hostname of the CommServ."""
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_hostname

    @property
    def commserv_name(self):
        """Returns the name of the CommServ."""
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_name

    @property
    def commserv_timezone(self):
        """Returns the time zone of the CommServ."""
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_timezone

    @property
    def commserv_timezone_name(self):
        """Returns the name of the time zone of the CommServ."""
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_timezone_name

    @property
    def commserv_version(self):
        """Returns the version installed on the CommServ.

            Example: 19

        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._commserv_version

    @property
    def version(self):
        """Returns the complete version info of the commserv

            Example: 11.19.1

        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._version_info

    @property
    def release_name(self):
        """Returns the complete release Name of the commserv

            Example: 2024E

        """
        if not self._commserv_details_loaded:
            self._get_commserv_details()
        return self._release_name

    @property
    def webconsole_hostname(self):
        """Returns the value of the host name of the webconsole used to connect to the Commcell."""
        return self._headers['Host']

    @property
    def auth_token(self):
        """Returns the Authtoken for the current session to the Commcell."""
        return self._headers['Authtoken']

    @property
    def commcell_username(self):
        """Returns the logged in user name"""
        return self._user

    @property
    def user_mappings(self) -> dict:
        """Returns the user mappings for the currently logged in user."""
        if self._user_mappings is None:
            self._user_mappings = self.wrap_request('GET', 'USER_MAPPINGS')
        return self._user_mappings

    @property
    def user_role(self) -> UserRole:
        """
        Returns the user role enum for the currently logged in user.

        Example: UserRole.MSP_ADMIN, UserRole.MSP_USER, etc ...
        """
        if self._user_role is None:
            self._user_role = UserRole(self.user_mappings.get('userRole', 5))
        return self._user_role

    @property
    def is_tenant(self) -> bool:
        """Returns True if the logged-in user is a company user"""
        return self.user_role in [UserRole.TENANT_USER, UserRole.TENANT_ADMIN]

    @property
    def is_tenant_level(self) -> bool:
        """Returns True if the logged-in user is at company level"""
        return bool(self.is_tenant or self.operating_company)

    @property
    def user_org(self) -> Organization | None:
        """
        Returns the organization object, the currently logged in user belongs to.

        Note: update operations might fail depending on the user role and permissions.
        """
        if 'providerId' not in self.user_mappings:
            return None
        if self._user_org is None:
            self._user_org = Organization(self, organization_id=self.user_mappings['providerId'])
            # need to directly use Organization class here, as /Organizations API may be restricted
            # but GET /Organization/{org_id} API response is always provided to all users
        return self._user_org

    @property
    def device_id(self):
        """Returns the value of the Device ID attribute."""
        try:
            return self._device_id
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def name_change(self):
        """Returns an instance of Namechange class"""
        return NameChange(self)

    @property
    def clients(self):
        """Returns the instance of the Clients class."""
        try:
            if self._clients is None:
                self._clients = Clients(self)

            return self._clients
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def commserv_cache(self):
        """Returns the instance of the CommServeCache  class."""
        try:
            if self._commserv_cache is None:
                self._commserv_cache = CommServeCache(self)

            return self._commserv_cache
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def index_servers(self):
        """Returns the instance of the Index Servers class."""
        try:
            if self._index_servers is None:
                self._index_servers = IndexServers(self)

            return self._index_servers
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def hac_clusters(self):
        """Returns the instance of the HAC Clusters class."""
        try:
            if self._hac_clusters is None:
                self._hac_clusters = HACClusters(self)

            return self._hac_clusters
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def network_topologies(self):
        """Returns the instance of the Network Topologies class."""
        try:
            if self._nw_topo is None:
                self._nw_topo = NetworkTopologies(self)

            return self._nw_topo
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def index_pools(self):
        """Returns the instance of the HAC Clusters class."""
        try:
            if self._index_pools is None:
                self._index_pools = IndexPools(self)

            return self._index_pools
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def media_agents(self):
        """Returns the instance of the MediaAgents class."""
        try:
            if self._media_agents is None:
                self._media_agents = MediaAgents(self)

            return self._media_agents
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def workflows(self):
        """Returns the instance of the Workflows class."""
        try:
            if self._workflows is None:
                self._workflows = WorkFlows(self)

            return self._workflows
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def alerts(self):
        """Returns the instance of the Alerts class."""
        try:
            if self._alerts is None:
                self._alerts = Alerts(self)

            return self._alerts
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def disk_libraries(self):
        """Returns the instance of the DiskLibraries class."""
        try:
            if self._disk_libraries is None:
                self._disk_libraries = DiskLibraries(self)

            return self._disk_libraries
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def tape_libraries(self):
        """Returns the instance of the TapeLibraries class"""
        if self._tape_libraries is None:
            self._tape_libraries = TapeLibraries(self)
        return self._tape_libraries

    @property
    def storage_policies(self):
        """Returns the instance of the StoragePolicies class."""
        return self.policies.storage_policies

    @property
    def schedule_policies(self):
        """Returns the instance of the SchedulePolicies class."""
        return self.policies.schedule_policies

    @property
    def schedules(self):
        """Returns the instance of the Schedules class."""
        try:
            if self._schedules is None:
                self._schedules = Schedules(self)

            return self._schedules
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def policies(self):
        """Returns the instance of the Policies class."""
        try:
            if self._policies is None:
                self._policies = Policies(self)

            return self._policies
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def deduplication_engines(self):
        """Returns the instance of the Deduplicationengines class."""
        try:
            if self._deduplication_engines is None:
                self._deduplication_engines = DeduplicationEngines(self)
            return self._deduplication_engines
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def user_groups(self):
        """Returns the instance of the UserGroups class."""
        try:
            if self._user_groups is None:
                self._user_groups = UserGroups(self)

            return self._user_groups
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def domains(self):
        """Returns the instance of the UserGroups class."""
        try:
            if self._domains is None:
                self._domains = Domains(self)

            return self._domains
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def client_groups(self):
        """Returns the instance of the ClientGroups class."""
        try:
            if self._client_groups is None:
                self._client_groups = ClientGroups(self)

            return self._client_groups
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def global_filters(self):
        """Returns the instance of the GlobalFilters class."""
        try:
            if self._global_filters is None:
                self._global_filters = GlobalFilters(self)

            return self._global_filters
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def datacube(self):
        """Returns the instance of the Datacube class."""
        try:
            if self._datacube is None:
                self._datacube = Datacube(self)

            return self._datacube
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def content_analyzers(self):
        """Returns the instance of the ContentAnalyzers class."""
        try:
            if self._content_analyzers is None:
                self._content_analyzers = ContentAnalyzers(self)

            return self._content_analyzers
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def resource_pool(self):
        """Returns the instance of the ResourcePools class."""
        try:
            if self._resource_pool is None:
                self._resource_pool = ResourcePools(self)
            return self._resource_pool
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def activate(self):
        """Returns the instance of the ContentAnalyzers class."""
        try:
            if self._activate is None:
                self._activate = Activate(self)

            return self._activate
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def threat_indicators(self):
        """Returns the instance of Servers class"""
        try:
            if self._threat_indicators is None:
                self._threat_indicators = TAServers(self)

            return self._threat_indicators

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def export_sets(self):
        """Returns the instance of the ExportSets class."""
        try:
            if self._export_sets is None:
                self._export_sets = ExportSets(self)
            return self._export_sets
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def plans(self):
        """Returns the instance of the Plans class."""
        try:
            if self._plans is None:
                self._plans = Plans(self)

            return self._plans
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def job_controller(self):
        """Returns the instance of the Jobs class."""
        try:
            if self._job_controller is None:
                self._job_controller = JobController(self)

            return self._job_controller
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def users(self):
        """Returns the instance of the Users class."""
        try:
            if self._users is None:
                self._users = Users(self)

            return self._users
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def roles(self):
        """Returns the instance of the Roles class."""
        try:
            if self._roles is None:
                self._roles = Roles(self)

            return self._roles
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def credentials(self):
        """Returns the instance of the Credentials class."""
        try:
            if self._credentials is None:
                self._credentials = Credentials(self)

            return self._credentials
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def download_center(self):
        """Returns the instance of the DownloadCenter class."""
        try:
            if self._download_center is None:
                self._download_center = DownloadCenter(self)

            return self._download_center
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def organizations(self):
        """Returns the instance of the Organizations class."""
        try:
            if self._organizations is None:
                self._organizations = Organizations(self)

            return self._organizations
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def tags(self):
        """Returns the instance of the tags class."""
        try:
            if self._tags is None:
                self._tags = Tags(self)

            return self._tags
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def storage_pools(self):
        """Returns the instance of the StoragePools class."""
        try:
            if self._storage_pools is None:
                self._storage_pools = StoragePools(self)

            return self._storage_pools
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def monitoring_policies(self):
        """Returns the instance of the MonitoringPolicies class."""
        try:
            if self._monitoring_policies is None:
                self._monitoring_policies = MonitoringPolicies(self)

            return self._monitoring_policies
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def operation_window(self):
        """Returns the instance of the OperationWindow class."""
        try:
            if self._operation_window is None:
                self._operation_window = OperationWindow(self)
            return self._operation_window
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def activity_control(self):
        """Returns the instance of the ActivityControl class."""
        try:
            if self._activity_control is None:
                self._activity_control = ActivityControl(self)

            return self._activity_control
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def event_viewer(self):
        """Returns the instance of the Event Viewer class."""
        try:
            if self._events is None:
                self._events = Events(self)

            return self._events
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def array_management(self):
        """Returns the instance of the ArrayManagement class."""
        try:
            if self._array_management is None:
                self._array_management = ArrayManagement(self)

            return self._array_management
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def disasterrecovery(self):
        """Returns the instance of the DisasterRecovery class."""
        try:
            if self._disaster_recovery is None:
                self._disaster_recovery = DisasterRecovery(self)

            return self._disaster_recovery
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def identity_management(self):
        """Returns the instance of the IdentityManagementApps class."""
        try:
            if self._identity_management is None:
                self._identity_management = IdentityManagementApps(self)

            return self._identity_management
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def system(self):
        """Returns the instance of the System class."""
        try:
            if self._system is None:
                self._system = System(self)

            return self._system
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def commserv_client(self):
        """Returns the instance of the Client class for the CommServ client."""
        if not self._commserv_details_loaded:
            self._get_commserv_details()

        if self._commserv_client is None:
            self._commserv_client = self.clients.get(self.commcell_id)
        return self._commserv_client

    @property
    def commcell_migration(self):
        """Returns the instance of the CommcellMigration class"""
        try:
            if self._commcell_migration is None:
                self._commcell_migration = CommCellMigration(self)

            return self._commcell_migration
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def grc(self):
        """Returns the instance of the GlobalRepositoryCell class"""
        try:
            if self._grc is None:
                self._grc = GlobalRepositoryCell(self)

            return self._grc
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def registered_commcells(self):
        """
        Returns the dictionary consisting of all registered commcells and their info

        dict - consists of all registered commcells
            {
                "commcell_name1:{
                    details related to commcell_name1
                },
                "commcell_name2:{
                    details related to commcell_name2
                }
            }
        """
        if self._registered_commcells is None:
            self._registered_commcells = self._get_registered_commcells()
        return self._registered_commcells

    @property
    def replication_groups(self):
        """Returns the instance of ReplicationGroups class"""
        try:
            if self._replication_groups is None:
                self._replication_groups = ReplicationGroups(self)
            return self._replication_groups

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def failover_groups(self):
        """Returns the instance of FailoverGroups class"""
        try:
            if self._failover_groups is None:
                self._failover_groups = FailoverGroups(self)
            return self._failover_groups

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def recovery_targets(self):
        """Returns the instance of RecoverTargets class"""
        try:
            if self._recovery_targets is None:
                self._recovery_targets = RecoveryTargets(self)

            return self._recovery_targets

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def cleanroom_recovery_groups(self):
        """Returns the instance of RecoveryGroups class"""
        try:
            if self._recovery_groups is None:
                self._recovery_groups = RecoveryGroups(self)

            return self._recovery_groups

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def cleanroom_targets(self):
        """Returns the instance of RecoveryTargets class"""
        try:
            if self._cleanroom_targets is None:
                self._cleanroom_targets = CleanroomTargets(self)

            return self._cleanroom_targets

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def blr_pairs(self):
        """Returns the instance of BLRPairs class"""
        try:
            if self._blr_pairs is None:
                self._blr_pairs = BLRPairs(self)

            return self._blr_pairs

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def backup_network_pairs(self):
        """Returns the instance of BackupNetworkPairs class"""
        try:
            if self._backup_network_pairs is None:
                self._backup_network_pairs = BackupNetworkPairs(self)

            return self._backup_network_pairs

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def reports(self):
        """Returns the instance of the Report class"""
        try:
            if self._reports is None:
                self._reports = report.Report(self)
            return self._reports
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def job_management(self):
        """Returns the instance of the JobManagement class."""
        try:
            if not self._job_management:
                self._job_management = JobManagement(self)
            return self._job_management
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def commserv_metadata(self):
        """Returns the metadata of the commserv."""
        if self._commserv_metadata is None:
            self._commserv_metadata = self._get_commserv_metadata()
        return self._commserv_metadata

    @property
    def commserv_oem_id(self):
        """Returns the OEM ID of the commserve"""
        try:
            if self._commserv_oem_id is None:
                self._commserv_oem_id = self._get_commserv_oem_id()

            return self._commserv_oem_id
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def metallic(self):
        """Returns the instance of the Metallic class."""
        try:
            if self._metallic is None:
                self._metallic = Metallic(self)

            return self._metallic
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def is_privacy_enabled(self):
        """Method to return if the privacy is enabled at commcell level or not"""
        if self._commcell_properties is None:
            self.get_commcell_properties()

        self._privacy = self._commcell_properties.get('enablePrivacy')

        return self._privacy

    @property
    def key_management_servers(self):
        """Returns the instance of the KeyManagementServers class."""
        try:
            if self._kms is None:
                self._kms = KeyManagementServers(self)

            return self._kms
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def regions(self):
        """Returns the instance of the Regions class."""
        try:
            if self._regions is None:
                self._regions = Regions(self)

            return self._regions
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def snmp_configurations(self):
        """Returns the instance of the SNMPConfigurations class."""
        try:
            if self._snmp_configurations is None:
                self._snmp_configurations = SNMPConfigurations(self)
            return self._snmp_configurations
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def service_commcells(self):
        """Returns the instance of the ServiceCommcells class."""
        try:
            if self._service_commcells is None:
                self._service_commcells = ServiceCommcells(self)
            return self._service_commcells
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def logout(self):
        """Logs out the user associated with the current instance."""
        if self._headers['Authtoken'] is None:
            return 'User already logged out.'

        output = self._cvpysdk_object._logout()
        self._remove_attribs_()
        return output

    def request(self, request_type, request_url, request_body=None):
        """Runs the request of the type specified on the request URL, with the body passed
            in the arguments.

            Args:
                request_type    (str)   --  type of HTTP request to run on the Commcell

                    e.g.;

                        - POST

                        - GET

                        - PUT

                        - DELETE

                request_url     (str)   --  API name to run the request on with params, if any

                    e.g.;

                        - Backupset

                        - Agent

                        - Client

                        - Client/{clientId}

                        - ...

                        etc.

                request_body    (dict)  --  JSON request body to pass along with the request

                    default: None

            Returns:
                object  -   the response received from the server

        """
        request_url = self._web_service + request_url

        _, response = self._cvpysdk_object.make_request(
            request_type.upper(), request_url, request_body
        )

        return response

    def wrap_request(
            self, method: str, service_key: str, fill_params: tuple = None,
            req_kwargs: dict = None, **wrap_kwargs
        ):
        """
        Wraps the request to the Commcell in a standard format for most API calls

        Args:
            method (str)        --  HTTP method to use for the request (e.g., 'GET', 'POST')

            service_key (str)   --  Key to access the request URL from services.py dict

            fill_params (tuple) --  Tuple of parameters to fill in the service URL, if it has any %s formatting

            req_kwargs (dict)   --  kwargs dict to pass to the request
                                    Example:
                                    {
                                        'payload': dict | str,
                                        'attempts': int,
                                        'headers': dict,
                                        'stream': bool,
                                        'files': dict[str, File],
                                        'remove_processing_info': bool,
                                    }

            wrap_kwargs:
                return_resp (bool)          --  If True, returns the response object directly
                                                else, returns response.json()
                                                default: False

                ignore_flag (bool)          --  If True, ignores the flag in the response
                                                default: False

                empty_check (bool)          --  If True, checks if the response is empty and raises an exception
                                                default: True

                error_check (bool)          --  If True, handles error in response dict and raises an sdk exception
                                                default: False for 'GET' requests, True for others
                                                         as GET responses usually don't have error messages

                error_read (callable)       --  How to read error code and message from response dict
                                                A Callable that returns error code, message from resp dict as arg
                                                default:
                                                    checks for ['error', 'errorCode', 'errorMessage', 'errorString',
                                                                'resultCode', 'resultMessage'] in resp_dict

                error_callback (callable)   --  What to do when error code is not 0
                                                A Callable that takes the error code and message as arguments and
                                                raises an SDKException if needed
                                                default:
                                                    raises SDKException(<default module>, <default code>, error_message)

                sdk_exception (tuple)       --  The Module and Error Code for default_error_callback
                                                default: ('Response', '101')

        """
        req_kwargs = req_kwargs or {}
        exc_module, exc_code = wrap_kwargs.get('sdk_exception', ('Response', '101'))

        def default_error_read(resp_dict) -> tuple[int, str]:
            """Default error reading function"""
            error_node = resp_dict
            if 'error' in resp_dict:
                error_node = resp_dict['error']
            code = error_node.get('errorCode', error_node.get('resultCode', -1))
            msg = error_node.get('errorMessage',
                error_node.get('errorString',
                    error_node.get('resultMessage', 'No error message in response')
                )
            )
            return code, msg

        def default_error_callback(error_code: int, error_msg: str):
            """Default error callback function"""
            raise SDKException(exc_module, exc_code, f'[{error_code}: {error_msg}]')

        ignore_flag = wrap_kwargs.get('ignore_flag', False)
        return_resp = wrap_kwargs.get('return_resp', False)
        empty_check = wrap_kwargs.get('empty_check', True)
        error_check = wrap_kwargs.get('error_check', method!='GET')
        error_read = wrap_kwargs.get('error_read', default_error_read)
        error_callback = wrap_kwargs.get('error_callback', default_error_callback)

        def error_handling(res):
            erc, erm = error_read(res.json())
            if erc != 0:
                error_callback(erc, erm)

        api_url = self._services[service_key]
        if fill_params:
            api_url = api_url % fill_params
        flag, response = self._cvpysdk_object.make_request(method, api_url, **req_kwargs)
        if (not flag) and (not ignore_flag):
            try:
                error_handling(response)
            except:
                raise SDKException('Response', '101', response.content)

        if return_resp and not error_check:
            return response

        try:
            response.json()
        except:
            raise SDKException('Response', '103', f'Received: {response.content}')

        if empty_check and not response.json():
            raise SDKException('Response', '102')

        if error_check:
            error_handling(response)

        return response if return_resp else response.json()

    @contextmanager
    def wrapped_request(self, method: str, service_key: str, fill_params: tuple = None, **wrap_kwargs):
        """
        Context manager to wrap the API response handling code after request

        Args:
            method (str)        --  HTTP method to use for the request (e.g., 'GET', 'POST')

            service_key (str)   --  Key to access the request URL from services.py dict

            fill_params (tuple) --  Tuple of parameters to fill in the service URL, if it has any %s formatting

            wrap_kwargs:
                req_kwargs (dict)   --  kwargs dict to pass to .make_request(...)

                See wrap_request() signature

        Yields:
            response object or response.json() based on wrap_kwargs['return_resp']

        Raises:
            SDKException with response.content / response json for debugging
            if any error raised inside the with block
        """
        resp = self.wrap_request(method, service_key, fill_params, **wrap_kwargs)
        try:
            yield resp
        except Exception as exp:
            debug_msg = resp if isinstance(resp, dict) else resp.content
            raise SDKException('Response', '104', f'Got response: {debug_msg}') from exp

    def send_mail(self, receivers, subject, body=None, copy_sender=False, is_html_content=True, **kwargs):
        """Sends a mail to the specified email address from the email asscoiated to this user

            Args:
                receivers       (list)  --  list of email addresses to whom the email is to
                be sent

                subject         (str)   --  subject of the email that is to be sent to the user

                body            (str)   --  email body that is to be included in the email

                copy_sender     (bool)  --  copies the sender in the html report that is sent

                is_html_content (bool)  --  determines if the email body has html content

                    True    -   the email body has html content

                    False   -   the email content is plain text

                attachments (list)      --  list of local filepaths to send as attachment

            Raises:
                SDKException:
                    if failed to send an email to specified user

                    if response is empty

                    if response is not success

        """
        if body is None:
            body = ''

        send_email_request = {
            "App_SendEmailReq": {
                "emailInfo": {
                    "subject": subject,
                    "body": body,
                    "copySender": copy_sender,
                    "isHTML": is_html_content,
                    "toEmail": [
                        {
                            "emailAddress": email
                        } for email in receivers
                    ]
                }
            }
        }
        if attachments := kwargs.get('attachments'):
            send_email_request['App_SendEmailReq']['emailInfo']['attachments'] = [
                {"attachmentPath": path} for path in attachments
            ]

        response_json = self._qoperation_execute(send_email_request)
        if response_json.get('errorCode', 0) != 0:
            raise SDKException(
                'Commcell',
                '104',
                'Error: "{}"'.format(response_json['errorMessage'])
            )

    def refresh(self):
        """Refresh the properties of the Commcell."""
        
        if not self._commserv_details_set:
            self._commserv_details_loaded = False
        self._clients = None
        self._commserv_cache = None
        self._remote_cache = None
        self._media_agents = None
        self._workflows = None
        self._alerts = None
        self._disk_libraries = None
        self._tape_libraries = None
        self._storage_policies = None
        self._schedule_policies = None
        self._schedules = None
        self._user_groups = None
        self._domains = None
        self._client_groups = None
        self._global_filters = None
        self._datacube = None
        self._activate = None
        self._threat_indicators = None
        self._content_analyzers = None
        self._resource_pool = None
        self._plans = None
        self._job_controller = None
        self._users = None
        self._roles = None
        self._credentials = None
        self._download_center = None
        self._organizations = None
        self._policies = None
        self._storage_pools = None
        self._activity_control = None
        self._events = None
        self._monitoring_policies = None
        self._array_management = None
        self._disaster_recovery = None
        self._operation_window = None
        self._commserv_client = None
        self._identity_management = None
        self._commcell_migration = None
        self._grc = None
        self._registered_commcells = None
        self._index_servers = None
        self._hac_clusters = None
        self._nw_topo = None
        self._index_pools = None
        self._deduplication_engines = None
        self._tfa = None
        self._tags = None
        self._additional_settings = None
        self._snmp_configurations = None
        self._service_commcells = None
        self._user_mappings = None
        self._user_role = None
        self._user_org = None

    def get_remote_cache(self, client_name):
        """Returns the instance of the RemoteCache  class."""
        try:
            self._remote_cache = RemoteCache(self, client_name)
            return self._remote_cache

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def run_data_aging(
            self,
            copy_name=None,
            storage_policy_name=None,
            is_granular=False,
            include_all=True,
            include_all_clients=False,
            select_copies=False,
            prune_selected_copies=False,
            schedule_pattern=None):
        """
        Runs the Data Aging from Commcell,SP and copy level


        """
        if storage_policy_name is None:
            copy_name = ""
            storage_policy_name = ""

        if copy_name is None:
            copy_name = ""

        request_json = {
            "taskInfo": {
                "associations": [],
                "task": {
                    "taskType": 1,
                    "initiatedFrom": 2,
                    "policyType": 0,
                    "alert": {
                        "alertName": ""
                    },
                    "taskFlags": {
                        "isEdgeDrive": False,
                        "disabled": False
                    }
                },
                "subTasks": [
                    {
                        "subTaskOperation": 1,
                        "subTask": {

                            "subTaskType": 1,
                            "operationType": 4018
                        },

                        "options": {
                            "adminOpts": {
                                "dataAgingOption": {
                                    "selectCopies": select_copies,
                                    "includeAllClients": include_all_clients,
                                    "pruneSelectedCopies": prune_selected_copies,
                                    "isGranular": is_granular,
                                    "includeAll": include_all,
                                    "archiveGroupCopy": [
                                        {
                                            "copyName": copy_name,
                                            "storagePolicyName": storage_policy_name
                                        }
                                    ]
                                }
                            }
                        }
                    }
                ]
            }
        }

        if schedule_pattern:
            request_json = SchedulePattern().create_schedule(request_json, schedule_pattern)

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['CREATE_TASK'], request_json
        )

        if flag:
            if response.json():
                if "jobIds" in response.json():
                    from .job import Job
                    return Job(self, response.json()['jobIds'][0])

                elif "errorCode" in response.json():
                    error_message = response.json()['errorMessage']
                    o_str = 'Error: "{0}"'.format(error_message)
                    raise SDKException('Commcell', '105', o_str)

                elif "taskId" in response.json():
                    return Schedules(self).get(task_id=response.json()['taskId'])

                else:
                    raise SDKException('Commcell', '105')

            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_saml_token(self, validity=30):
        """Returns the SAML token for the currently logged-in user.

            Args:
                validity    (int)   --  validity of the SAML token, **in minutes**

                    default: 30

            Returns:
                str     -   SAML token string received from the server

        """
        flag, response = self._cvpysdk_object.make_request(
            'GET',
            self._services['GET_SAML_TOKEN'] % validity
        )

        if flag:
            if response.json():
                response = response.json()
                token = response.get('token')

                if token:
                    return token
                else:
                    error_message = response['errList'][0]['errLogMessage']
                    error_code = response['errList'][0]['errorCode']

                    if 'relogin required' in error_message.lower():
                        self._headers['Authtoken'] = self._cvpysdk_object._renew_login_token(5)
                        return self.get_saml_token(validity)

                    raise SDKException(
                        'Commcell',
                        '106',
                        'Error Code: {0}\nError Message: {1}'.format(error_code, error_message)
                    )
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_additional_setting(self, category, key_name, data_type, value):
        """Adds registry key to the commserve property.

            Args:
                category    (str)   --  Category of registry key

                key_name    (str)   --  Name of the registry key

                data_type   (str)   --  Data type of registry key

                    Accepted Values:
                        - BOOLEAN
                        - INTEGER
                        - STRING
                        - MULTISTRING
                        - ENCRYPTED

                value   (str)   --  Value of registry key

            Returns:
                None

            Raises:
                SDKException:
                    if failed to add

                    if response is empty

                    if response code is not as expected

        """
        self.commserv_client.add_additional_setting(category, key_name, data_type, value)
        self._additional_settings = None

    def delete_additional_setting(self, category, key_name):
        """Deletes registry key from the commserve property.

            Args:
                category    (str)   --  Category of registry key

                key_name    (str)   --  Name of the registry key

            Returns:
                None

            Raises:
                SDKException:
                    if failed to delete

                    if response is empty

                    if response code is not as expected

        """
        self.commserv_client.delete_additional_setting(category, key_name)
        self._additional_settings = None

    def get_configured_additional_setting(self) -> list:
        """Method to get configured additional settings name"""
        return self.commserv_client.get_configured_additional_settings()

    @property
    def additional_settings(self) -> dict:
        """
        property to store dict of additional settings configured on commcell

        Example:
            {
                'keyName': ('relativepath', 'keyName', 'type', 'value'),
                'keyName1': ('relativepath1', 'keyName1', 'type1', 'value1'),
                ...
            }
        """
        if self._additional_settings is None:
            self._additional_settings = {
                cs_key.get('keyName'): cs_key for cs_key in self.get_configured_additional_setting()
            }
        return self._additional_settings

    def protected_vms(self, days, limit=100):
        """
        Returns all the protected VMs for the particular client for passed days
        Args:
            days: Protected VMs for days
                ex: if value is 30 , returns VM protected in past 30 days

            limit: Number of Protected VMs
                ex: if value is 50, returns 50 protected vms are returned
                    if value is 0, all the protected vms are returned
                    default value is 100

        Returns:
                vm_dict -  all properties of VM protected for passed days

        """

        from_time, to_time = self._convert_days_to_epoch(days)
        self._PROTECTED_VMS = self._services['PROTECTED_VMS'] % (from_time, to_time, limit)
        flag, response = self._cvpysdk_object.make_request(
            'GET',
            self._PROTECTED_VMS
        )

        if flag:
            if response.json():
                return response.json()
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def sync_remote_cache(self, client_list=None, schedule_pattern=None):
        """Syncs remote cache

            Args:

                client_list (list) --  list of client names.
                Default is None. By default all remote cache clients are synced

                schedule_pattern (dict)        --  Pattern to schedule Sync Job

            Returns:
                object - instance of the Job class for sync job

            Raises:
                SDKException:
                    if sync job failed

                    if response is empty

                    if response is not success

                    if another sync job is running with the given client

        """
        download = Download(self)
        return download.sync_remote_cache(
            client_list=client_list, schedule_pattern=schedule_pattern)

    def download_software(self,
                          options=None,
                          os_list=None,
                          service_pack=None,
                          cu_number=1,
                          sync_cache=True,
                          sync_cache_list=None,
                          schedule_pattern=None):
        """Downloads the os packages on the commcell

            Args:

                options      (enum)            --  Download option to download software

                os_list      (list of enum)    --  list of windows/unix packages to be downloaded

                service_pack (int)             --  service pack to be downloaded

                cu_number (int)                --  maintenance release number

                sync_cache (bool)              --  True if download and sync
                                                   False only download
                
                sync_cache_list (list)         --  list of names of remote caches to sync
                                                   use None to sync all caches

            Returns:
                object - instance of the Job class for this download job

            Raises:
                SDKException:
                    if Download job failed

                    if response is empty

                    if response is not success

                    if another download job is running

            Usage:

            -   if download_software is not given any parameters it takes default value of latest
                service pack for options and downloads WINDOWS_64 package

                >>> commcell_obj.download_software()

            -   DownloadOptions and DownloadPackages enum is used for providing input to the
                download software method, it can be imported by

                >>> from cvpysdk.deployment.deploymentconstants import DownloadOptions
                    from cvpysdk.deployment.deploymentconstants import DownloadPackages

            -   sample method calls for different options, for latest service pack

                >>> commcell_obj.download_software(
                        options=DownloadOptions.LATEST_SERVICEPACK.value,
                        os_list=[DownloadPackages.WINDOWS_64.value]
                        )

            -   For Latest hotfixes for the installed service pack

                >>> commcell_obj.download_software(
                        options='DownloadOptions.LATEST_HOTFIXES.value',
                        os_list=[DownloadPackages.WINDOWS_64.value,
                                DownloadPackages.UNIX_LINUX64.value]
                        )

            -   For service pack and hotfixes

                >>> commcell_obj.download_software(
                        options='DownloadOptions.SERVICEPACK_AND_HOTFIXES.value',
                        os_list=[DownloadPackages.UNIX_MAC.value],
                        service_pack=13
                        )

                    **NOTE:** service_pack parameter must be specified for third option

        """
        download = Download(self)
        return download.download_software(
            options=options,
            os_list=os_list,
            service_pack=service_pack,
            cu_number=cu_number,
            sync_cache=sync_cache,
            sync_cache_list=sync_cache_list,
            schedule_pattern=schedule_pattern
        )

    def copy_software(self,
                      media_loc,
                      username=None,
                      password=None,
                      sync_cache=True,
                      sync_cache_list=None,
                      schedule_pattern=None):
        """copies media from the specified location on the commcell

                    Args:

                        media_loc      (str)           --  Media Location to be used for copy software

                        username       (str)           --  username to authenticate to external location

                        password       (str)           --  password to authenticate to external location

                        sync_cache (bool)              --  True if download and sync
                                                           False only download

                        sync_cache_list (list)         --  list of names of remote caches to sync
                                                   use None to sync all caches

                        schedule_pattern(dict)         --  pattern for schedule task


                    Returns:
                        object - instance of the Job class for this copy software job

                    Raises:
                        SDKException:
                            if Download job failed

                            if response is empty

                            if response is not success

                            if another download job is running
                    Usage:

                        -   if media_location directory is local to the machine - username and password is not needed

                            >>> commcell_obj.copy_software(media_loc = "C:\\Downloads\\Media")

                        -   if Media_location directory is remote- username and passsword(base 64 encoded) are needed
                            to authenticate the cache

                            >>> commcell_obj.copy_software(
                            media_loc = "\\subdomain.company.com\\Media",
                            username = "domainone\\userone",
                            password = "base64encoded password"
                            )
                """
        download = Download(self)
        return download.copy_software(
            media_loc=media_loc,
            username=username,
            password=password,
            sync_cache=sync_cache,
            sync_cache_list=sync_cache_list,
            schedule_pattern=schedule_pattern
        )

    def push_servicepack_and_hotfix(
            self,
            client_computers=None,
            client_computer_groups=None,
            all_client_computers=False,
            all_client_computer_groups=False,
            reboot_client=False,
            run_db_maintenance=True,
            maintenance_release_only=False,
            **kwargs):
        """triggers installation of service pack and hotfixes

        Args:
            client_computers    (list)      -- Client machines to install service pack on

            client_computer_groups (list)   -- Client groups to install service pack on

            all_client_computers (bool)     -- boolean to specify whether to install on all client
            computers or not

                default: False

            all_client _computer_groups (bool) -- boolean to specify whether to install on all
            client computer groups or not

                default: False

            reboot_client (bool)            -- boolean to specify whether to reboot the client
            or not

                default: False

            run_db_maintenance (bool)      -- boolean to specify whether to run db
            maintenance not

                default: True

            maintenance_release_only (bool) -- for clients of feature releases lesser than CS, this option
            maintenance release of that client FR, if present in cache
            **kwargs: (dict) -- Key value pairs for supporting conditional initializations
                Supported -
                schedule_pattern (dict)           -- Request JSON for scheduling the operation

        Returns:
            object - instance of the Job/Task class for this download

        Raises:
                SDKException:
                    if schedule is not of type dictionary

                    if Download job failed

                    if response is empty

                    if response is not success

                    if another download job is already running

        **NOTE:** push_serivcepack_and_hotfixes cannot be used for revision upgrades

        """
        schedule_pattern = kwargs.get("schedule_pattern", None)
        if schedule_pattern:
            if not isinstance(schedule_pattern, dict):
                raise SDKException("Commcell", "101")
        install = Install(self)
        return install.push_servicepack_and_hotfix(
            client_computers=client_computers,
            client_computer_groups=client_computer_groups,
            all_client_computers=all_client_computers,
            all_client_computer_groups=all_client_computer_groups,
            reboot_client=reboot_client,
            run_db_maintenance=run_db_maintenance,
            maintenance_release_only=maintenance_release_only,
            schedule_pattern=schedule_pattern,
            **kwargs
        )

    def install_software(
            self,
            client_computers=None,
            windows_features=None,
            unix_features=None,
            username=None,
            password=None,
            install_path=None,
            log_file_loc=None,
            client_group_name=None,
            storage_policy_name=None,
            sw_cache_client=None,
            **kwargs):
        """
        Installs the selected features in the selected clients
        Args:

            client_computers    (list)      -- list of hostnames/IP address to install the
            features on

                default : None

            windows_features (list of enum) -- list of windows features to be installed

                default : None

            unix_features (list of enum)    -- list of unix features to be installed

                default : None

            username    (str)               -- username of the machine to install features on

                default : None

            password    (str)               -- base64 encoded password

                default : None

            install_path (str)              -- Install to a specified path on the client

                 default : None

            log_file_loc (str)              -- Install to a specified log path on the client

                 default : None

            client_group_name (list)        -- List of client groups for the client

                 default : None

            storage_policy_name (str)       -- Storage policy for the default subclient

                 default : None

            sw_cache_client (str)           -- Remote Cache Client Name/ Over-riding Software Cache

                default : None (Use CS Cache by default)

            **kwargs: (dict) -- Key value pairs for supporting conditional initializations
            Supported -
            commserv_name (str) - Name of the CommServe (if user doesn't have view permission on CommServe)
            install_flags (dict)            -- dictionary of install flag values

                default : None

            Ex : install_flags = {"preferredIPfamily":2, "install32Base":True}

            db2_logs_location (dict) - dictionary of db2 logs location

                default : None
                
            Ex: db2_logs_location = {
                                    "db2ArchivePath": "/opt/Archive/",
                                    "db2RetrievePath": "/opt/Retrieve/",
                                    "db2AuditErrorPath": "/opt/Audit/"
                            }

        Returns:
                object - instance of the Job class for this install_software job

        Raises:
            SDKException:
                if install job failed

                if response is empty

                if response is not success

        Usage:

            -   UnixDownloadFeatures and WindowsDownloadFeatures enum is used for providing
                input to the install_software method, it can be imported by

                >>> from cvpysdk.deployment.deploymentconstants import UnixDownloadFeatures
                    from cvpysdk.deployment.deploymentconstants import WindowsDownloadFeatures

            -   sample method call

                >>> commcell_obj.install_software(
                                client_computers=[win_machine1, win_machine2],
                                windows_features=[WindowsDownloadFeatures.FILE_SYSTEM.value],
                                unix_features=None,
                                username='username',
                                password='password',
                                install_path='/opt/commvault',
                                log_file_loc='/var/log',
                                client_group_name=[My_Servers],
                                storage_policy_name='My_Storage_Policy',
                                sw_cache_client="remote_cache_client_name"
                                install_flags={"preferredIPFamily":2})

                    **NOTE:** Either Unix or Windows clients_computers should be chosen and
                    not both

        """
        install = Install(self)
        return install.install_software(
            client_computers=client_computers,
            windows_features=windows_features,
            unix_features=unix_features,
            username=username,
            password=password,
            install_path=install_path,
            log_file_loc=log_file_loc,
            client_group_name=client_group_name,
            storage_policy_name=storage_policy_name,
            sw_cache_client=sw_cache_client,
            **kwargs)

    @property
    def remote_cache_clients(self):
        """
            Fetches the List of Remote Cache configured for a particular Admin/Tenant
            :return: List of Remote Cache configured
        """
        try:
            if self._commserv_cache is None:
                self._commserv_cache = CommServeCache(self)

            return self._commserv_cache.get_remote_cache_clients()

        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def enable_auth_code(self):
        """Executes the request on the server to enable Auth Code for installation on commcell

            Args:
                None

            Returns:
                str     -   auth code generated from the server

            Raises:
                SDKException:
                    if failed to enable auth code generation

                    if response is empty

                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['GENERATE_AUTH_CODE'] % 0
        )

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Client', '102', 'Failed to set auth code, with error: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        return response.json()['organizationProperties']['authCode']

    def disable_auth_code(self):
        """
        Disables authcode requirement at Commcell level

        Raises:
            SDKException:
                if failed to enable auth code generation

                if response is empty

                if response is not success
        """
        request_json = {
            "organizationInfo": {
                "organization": {
                    "shortName": {
                        "id": 0
                    }
                },
                "organizationProperties": {
                    "enableAuthCodeGen": False
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ORGANIZATIONS'], request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Commcell', '108', 'Failed to disable authcode: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_shared_laptop(self):
        """Executes the request on the server to enable Shared Laptop on commcell

            Args:
                None

            Returns:
                None

            Raises:
                SDKException:
                    if response is empty
                    if failed to enable shared laptop
                    if response is not success
        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ENABLE_SHARED_LAPTOP']
        )

        if flag:
            if response.json():
                response = response.json().get('response', [{}])[0]
                if not response:
                    raise SDKException('Response', '102')
                if response.get('errorCode', -1) != 0:
                    raise SDKException(
                        'Response', '101', 'Failed to enable shared laptop')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_shared_laptop(self):
        """Executes the request on the server to disable Shared Laptop on commcell

            Args:
                None

            Returns:
                None

            Raises:
                SDKException:
                    if response is empty
                    if failed to disable shared laptop
                    if response is not success

        """
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['DISABLE_SHARED_LAPTOP']
        )

        if flag:
            if response.json():
                response = response.json().get('response', [{}])[0]
                if not response:
                    raise SDKException('Response', '102')
                if response.get('errorCode', -1) != 0:
                    raise SDKException(
                        'Response', '101', 'Failed to disable shared laptop')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_privacy(self):
        """Enables users to enable data privacy on commcell"""
        if self.is_privacy_enabled is True:
            return

        self.set_privacy(True)

    def disable_privacy(self):
        """Enables users to disable data privacy on commcell"""
        if self.is_privacy_enabled is False:
            return

        self.set_privacy(False)

    def set_privacy(self, value):
        """
        Method to enable/disble privacy
            Args:
                value (bool): True/False to enable/disable privacy

        Raises:
                SDKException:
                    if response is empty
                    if failed to disable privacy
                    if response is not success
        """
        url = self._services['PRIVACY_DISABLE']
        if value:
            url = self._services['PRIVACY_ENABLE']

        flag, response = self._cvpysdk_object.make_request(
            'PUT', url
        )

        if flag:
            if response and response.json():
                response = response.json().get('response', [{}])[0]
                if not response:
                    raise SDKException('Response', '102')
                if response.get('errorCode', -1) != 0:
                    error_string = response.json().get('errorString')
                    raise SDKException(
                        'Commcell', '108', error_string)
                self.get_commcell_properties()

            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_commcell_properties(self):
        """ Get Commcell properties

        Returns: (dict)
            "hostName": String,
            "enableSharedLaptopUsage": Boolean,
            "enableTwoFactorAuthentication": Boolean,
            "networkErrorRetryCount": Number,
            "useUPNForEmail": Boolean,
            "flags": Number,
            "description": String,
            "networkErrorRetryFreq": Number,
            "autoClientOwnerAssignmentType": Number,
            "networkErrorRetryFlag": Boolean,
            "allowUsersToEnablePasskey": Boolean,
            "autoClientOwnerAssignmentValue": String,
            "enablePrivacy": Boolean,
            "twoFactorAuthenticationInfo": {
                "mode": Number
            }
        """
        url = self._services['SET_COMMCELL_PROPERTIES']
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                self._commcell_properties = response.get("commCellInfo").get("generalInfo")
                return self._commcell_properties
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_commcell_organization_properties(self):
        """
            Get organization properties for the commcell
        return:
            dict of organization properties of commcell
        """
        url = self._services['ORGANIZATION'] % '0'
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                passkey_details = response.get('organizationInfo').get('organizationProperties')
                return passkey_details
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_email_settings(self):
        """
            Get Email Server (SMTP) setup for commcell
        return: (dict) Email server settings for commcell
        """
        url = self._services['EMAIL_SERVER']
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                return response
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def set_email_settings(self, smtp_server, sender_name, sender_email, **kwargs):
        """Set Email Server (SMTP) setup for commcell

            Args:
                smtp_server(str)    --  hostname of the SMTP server
                sender_name(str)    --  Name of the sender
                sender_email(str)   --  Email address of the sender to be used
                ** kwargs(dict)     --  Key value pairs for supported arguments
                Supported argument values:

                    enable_ssl(boolean) --  option to represent whether ssl is supported for the EMail Server
                                            Default value: False
                    start_tls (boolean) --  option to represent whether tls is supported for the EMail Server
                                            Default value: False
                    smtp_port(int)      --  Port number to be used by Email Server
                                            Default value: 25
                    username(str)       --  Username to be used
                    password(str)       --  Password to be used

            Returns:
                None

            Raises:
                SDKException:
                    if invalid argument type is passed
                    if failed to update Email server
                    if response is empty
                    if response is not success

        """

        if not (isinstance(smtp_server, str) and isinstance(sender_email, str)
                and isinstance(sender_name, str)):
            raise SDKException("Commcell", "101")

        enable_ssl = kwargs.get("enable_ssl", False)
        start_tls = kwargs.get("start_tls", False)
        smtp_port = kwargs.get("smtp_port", 25)
        username = kwargs.get("username", "")
        password = kwargs.get("password", "")

        if not (isinstance(enable_ssl, bool) and isinstance(smtp_port, int)
                and isinstance(username, str) and isinstance(password, str)):
            raise SDKException("Commcell", "101")

        request_json = {"smtpInfo":
                            {"enableSSL": enable_ssl,
                             "startTLS": start_tls,
                             "smtpServer": smtp_server,
                             "smtpPort": smtp_port,
                             "useAuthentication": False,
                             "maxMailServerSize": 0,
                             "userInfo": {
                                 "password": username,
                                 "userName": password
                             },
                             "senderInfo": {
                                 "senderName": sender_name,
                                 "senderAddress": sender_email
                             }
                             }
                        }
        url = self._services['EMAIL_SERVER']
        flag, response = self._cvpysdk_object.make_request(
            'POST', url, request_json
        )
        if flag:
            if response.json():
                error_code = response.json().get('errorCode', 0)
                if error_code != 0:
                    raise SDKException('Response', '101', self._update_response_(response.text))
                return
            raise SDKException('Response', '102')
        raise SDKException('Response', '101', self._update_response_(response.text))

    def get_password_encryption_config(self):
        """ Get the password encryption config for commcell
        returns: (dict)
            "keyFilePath": String,
            "keyProviderName": String,
            "isKeyMovedToFile": Boolean
        """
        pass__enc_config = {}

        url = self._services['PASSWORD_ENCRYPTION_CONFIG']
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                for key, value in response.items():
                    pass__enc_config.update({key: value})
                return pass__enc_config
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_security_associations(self):
        """ Get the security associations for commcell
            Returns: (dict)
                    {
                    'master': [
                                ['Array Management'],
                                ['Create Role', 'Edit Role', 'Delete Role'],
                                ['Master']
                            ],
                    'User2': [
                                ['View']
                            ]
                    }
         """
        security_associations = {}
        value_list = {}
        url = self._services['SECURITY_ASSOCIATION'] + '/1/2'
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                security_list = response.get('securityAssociations')[0].get('securityAssociations').get('associations')
                for list_item in security_list:
                    name = list_item.get('userOrGroup')[0].get('userGroupName') or \
                        list_item.get('userOrGroup')[0].get('userName') or \
                        list_item.get('userOrGroup')[0].get('providerDomainName') + '\\' + \
                        list_item.get('userOrGroup')[0].get('externalGroupName')
                    value = []
                    if list_item.get('properties').get('role'):
                        value.append(list_item.get('properties').get('role').get('roleName'))
                    elif list_item.get('properties').get('categoryPermission'):
                        for sub_list_item in list_item.get('properties').get('categoryPermission').get(
                                'categoriesPermissionList'):
                            value.append(sub_list_item.get('permissionName'))
                    if name in value_list:
                        value_list[name].append(value)
                        value_list[name].sort()
                    else:
                        value_list[name] = [value]
                    security_associations.update({name: value_list[name]})
                return security_associations
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_default_plan(self):
        """Executes the request on the server to get Default Plan at commcell level.
           This is independent of the organization, as id is 0.
           returns: (list of dictionaries)
                 [
                 { "subtype": 'File system plan', "plan": { "planName": "Gold plan", "planId": 2 } }
                ]
         """
        default_plan_details = []
        plan_sub_type = {
            16777223: 'DLO plan',
            33554437: 'Server plan',
            33554439: 'Laptop plan',
            33579013: 'Database plan',
            67108869: 'Snap plan',
            50331655: 'File system plan',
            83886085: 'VSA system plan',
            83918853: 'VSA Replication plan',
            100859907: 'ExchangeUser plan',
            100794372: 'ExchangeJournal plan',
            117506053: 'DataClassification plan',
            1: 'Ediscovery plan'
        }
        url = self._services['ORGANIZATION'] % '0' + '/defaultplan'
        flag, response = self._cvpysdk_object.make_request('GET', url=url)

        if flag:
            if response.json():
                response = response.json()
                plan_details = response.get('organizationInfo').get('organizationProperties')
                if "defaultPlans" in plan_details:
                    plan_list = plan_details.get('defaultPlans')
                    for default_plan in plan_list:
                        default_plan_details.append({"subtype": plan_sub_type.get(default_plan.get('subtype')),
                                                     "plan": {
                                                         "planName": default_plan.get('plan').get('planName'),
                                                         "planId": default_plan.get('plan').get('planId')}
                                                     })
                return default_plan_details
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def set_default_plan(self, plan_name):
        """Executes the request on the server to set Default Plan at commcell level.
            This is independent of the organization, as id is 0.

            Args:
                plan_name (str)    - Plan name

            Returns:
                None

            Raises:
                SDKException:
                    if failed to set Default plan

                    if response is empty

                    if response is not success

        """

        request_json = {
            "organizationInfo": {
                "organization": {
                    "shortName": {
                        "id": 0
                    }
                },
                "organizationProperties": {
                    "defaultPlansOperationType": 1,
                    "defaultPlans": [
                        {
                            "plan": {
                                "planName": plan_name
                            }
                        }
                    ]
                }
            }
        }

        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ORGANIZATIONS'], request_json
        )

        if flag:
            if response.json():
                error_code = response.json()['error']['errorCode']

                if error_code != 0:
                    raise SDKException(
                        'Client', '102', 'Failed to set default plan, with error: "{0}"'.format(
                            response.json()['error']['errorMessage']
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def execute_qcommand(self, command, input_xml=None):
        """Executes the ExecuteQCommand API on the commcell.

            Args:
                command     (str)   --  qcommand to be executed

                input_xml   (str)   --  xml body (if applicable)

                    default:    None

            Returns:
                object  -   requests.Response object

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

            Deprecated:
                This method is deprecated and will be removed in a future version.
                Use `execute_qcommand_v2` instead.

        """
        from urllib.parse import (urlencode, quote)

        headers = self._headers.copy()
        headers['Content-type'] = 'application/x-www-form-urlencoded'

        payload = {
            'command': command
        }

        if input_xml:
            payload['inputRequestXML'] = input_xml

        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['EXEC_QCOMMAND'], urlencode(payload, quote_via=quote), headers=headers
        )

        if flag:
            return response
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def execute_qcommand_v2(self, command, input_data=None):
        """Executes the QCommand API on the commcell.

            Args:
                command     (str)   --  qcommand to be executed

                input_data   (str/dict)  --  xml/json/dict body (if applicable)

            Returns:
                object  -   requests.Response object

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """

        headers = self._headers.copy()
        dict_data = dict()

        if input_data and not isinstance(input_data, dict):
            try:
                dict_data = xmltodict.parse(input_data, attr_prefix='')
            except Exception as e:
                try:
                    import json
                    dict_data = json.loads(input_data)
                except Exception as e:
                    raise SDKException('Commcell', '107', 'Unable to parse the input data as either XML or JSON')

        flag, response = self._cvpysdk_object.make_request(
            'POST', f"{self._services['QCOMMAND']}/{command}", dict_data, headers=headers
        )

        if flag:
            return response
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def add_associations_to_saml_app(self, saml_app_name, saml_app_key, props, user_to_be_added):
        """adds the given  user under associations tab of the saml app
            Args:
                saml_app_name   (str)   : SAML app name to add associations for

                saml_app_key    (str)   :app key of the SAML app

                props   (str)   :properties to be included in the XML request

                user_to_be_added    (str)   : user to be associated with

            Raises:
                SDKException:
                    if input data is invalid

                    if response is empty

                    if response is not success
        """

        xml_execute_command = """
            <App_SetClientThirdPartyAppPropReq opType="3">
            <clientThirdPartyApps appDescription="" appKey="{0}" appName="{1}" appType="2" flags="2" isCloudApp="0" isEnabled="1">
                {2}
                <UserMappings/>
                <assocTree _type_="13" userName="{3}"/>
            </clientThirdPartyApps>
        </App_SetClientThirdPartyAppPropReq>
        	"""\
            .format(str(saml_app_key), saml_app_name, props, user_to_be_added)
        self._qoperation_execute(xml_execute_command)

    def _get_registered_commcells(self):
        """
        Gets the registered commcells
        (Not to be confused with service commcells, use commcell.service_commcells class for that)
        
        Returns:
            dict - consists of all registered routing commcells
                {
                    "commcell_name1": {
                        related information of commcell1
                    },
                    "commcell_name2:: {
                        related information of commcell2
                    }
                }
        Raises:
            SDKException:
                if response is empty

                if response is not success
        """
        flag, response = self._cvpysdk_object.make_request('GET', self._services['GET_REGISTERED_COMMCELLS'])
        if flag:
            if response.json() and 'commcellsList' in response.json():
                register_commcells_dict = {}

                for registered_commcell in response.json()['commcellsList']:
                    register_commcells_dict[registered_commcell['commCell']['commCellName']] = registered_commcell
                return register_commcells_dict
            else:
                return {}
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def register_commcell(self, commcell_name, admin_username, admin_password, **kwargs):
        """
        Registers a commcell
        (for service commcell registration, use service_commcells.add)

        Args:

            commcell_name   (str)           --  commandcenter hostname of the commcell or
                                                the complete commandcenter URL

            admin_username   (str)          --  username of the user who has administrative
                                                rights on a commcell

            admin_password  (str)           --  password of the user specified

        Raises:

            SDKException:

                if the registration fails
                if response is empty
                if there is no response

        """
        commcell_url = commcell_name.lower()
        if 'http' not in commcell_name:
            commcell_url = f"https://{commcell_name}/commandcenter"

        payload = {
            "serviceCommcelWebconsoleUrl": commcell_url,
            "username": admin_username,
            "isIDPCommcell": False,
            "displayName": kwargs.get('commcell_displayname'),
            "userOrGroup": [],
            "password": b64encode(admin_password.encode()).decode()
        } | kwargs.get('custom_payload', {})

        self.wrap_request(
            'POST', 'REGISTRATION',
            req_kwargs={'payload': payload},
            sdk_exception=('CommcellRegistration', '101')
        )
        self._registered_commcells = None

    def get_redirect_list(self, login: str = None):
        """
        Gets the list of redirects available for user based on login_name or email provided

        Args:
            login      (str)   --   Login name or email of the user

        Raises:
            if the response is empty
            if there is no response

        Returns:
            list_of_service_commcells   (list)  -- list of service commcells

        """
        login = login or self.commcell_username
        login = login.lower()
        flag, response = self._cvpysdk_object.make_request('GET', self._services['REDIRECT_LIST'] % login)
        if flag:
            if response.json() and 'AvailableRedirects' in response.json():
                service_commcell_list = []
                for ser_comm in response.json()['AvailableRedirects']:
                    service_commcell_list.append(
                        urlparse(ser_comm['redirectUrl']).netloc
                    )
                return service_commcell_list
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    @property
    def is_service_commcell(self):
        """Returns the is_service_commcell property."""
        return self._is_service_commcell

    @property
    def master_saml_token(self):
        """Returns the saml token of master commcell."""
        return self._master_saml_token

    @property
    def master_commcell(self):
        """Returns the master commcell object."""
        return self._master_commcell

    @property
    def two_factor_authentication(self):
        """Returns the instance of the TwoFactorAuthentication class"""
        try:
            if self._tfa is None:
                self._tfa = TwoFactorAuthentication(self)
            return self._tfa
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    @property
    def is_tfa_enabled(self):
        """
        Returns the status of two factor authentication for this commcell

            bool    --  status of tfa.
        """
        return self.two_factor_authentication.is_tfa_enabled

    @property
    def tfa_enabled_user_groups(self):
        """
        Returns the list of user group names for which two factor authentication is enabled.
         only for user group inclusion tfa.
            eg:-
            [
                {
                "userGroupId": 1,
                "userGroupName": "dummy"
                }
            ]
        """
        return self.two_factor_authentication.tfa_enabled_user_groups

    @property
    def is_linux_commserv(self):
        """
        Returns true if CommServer is installed on the linux machine

        Returns None if unable to determine the CommServ OS type

        **Note** To determine CommServ OS type logged in user
        should have access on CommServ client
        """
        if self._is_linux_commserv is None and self.clients.has_client(self.commserv_name):
            self._is_linux_commserv = 'unix' in self.commserv_client.os_info.lower()
        return self._is_linux_commserv

    @property
    def default_timezone(self):
        """Returns the default timezone used for all the operations performed via cvpysdk"""
        return 'UTC' if self.is_linux_commserv else '(UTC) Coordinated Universal Time'

    @property
    def is_passkey_enabled(self):
        """Returns True if Passkey is enabled on commcell"""
        org_prop = self.get_commcell_organization_properties()
        return True if org_prop.get('advancedPrivacySettings', {}).get('authType', 0) == 2 else False

    @property
    def databases(self):
        """Returns the list of databases associated with the Commcell"""
        if self._databases is None:
            flag, response = self._cvpysdk_object.make_request('GET', self._services['DATABASES'])
            if flag:
                if response.json():
                    response = response.json()
                    self._databases = [database['backupset']['backupsetName'] for database in response['dbInstance']]
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        return self._databases

    @property
    def database_instances(self):
        """Returns the list of database instances associated with the Commcell"""
        if self._db_instances is None:
            flag, response = self._cvpysdk_object.make_request('GET', self._services['DB_INSTANCES'])
            if flag:
                if response.json():
                    response = response.json()
                    self._db_instances = [instance['instance']['instanceName'] for instance in response['dbInstance']]
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        return self._db_instances

    @property
    def database_instant_clones(self):
        """Returns the list of database instant clones jobs active on the Commcell"""
        if self._db_instant_clones is None:
            flag, response = self._cvpysdk_object.make_request('GET', self._services['DB_INSTANT_CLONES'])
            if flag:
                if response.json():
                    response = response.json()
                    self._db_instant_clones = [clone['cloneJobId'] for clone in response['clones']]
                else:
                    raise SDKException('Response', '102')
            else:
                raise SDKException('Response', '101', self._update_response_(response.text))
        return self._db_instant_clones

    def enable_tfa(self, user_groups=None, usernameless=False, passwordless=False):
        """
        Enables two factor authentication option on this commcell.

        Args:
            user_groups     (list)  --  user group names for which tfa needs to be enabled.
            usernameless    (bool)  --  allow usernameless login if True
            passwordless    (bool)  --  allow passwordless login if True

        Returns:
            None
        """
        self.two_factor_authentication.enable_tfa(
            user_groups=user_groups, usernameless=usernameless, passwordless=passwordless
        )

    def disable_tfa(self):
        """
        Disables two factor authentication on this commcell.

        Returns:
            None
        """
        self.two_factor_authentication.disable_tfa()

    def _get_commserv_metadata(self):
        """loads  the metadata of the CommServ, the Commcell class instance is initialized for,
            and updates the class instance attributes.

            Returns:
                commserv_metadata (dict) : returns a dict containing commserv_redirect_url and commserv_certificate

            Raises:
                SDKException:
                    if failed to get commserv details


                    if response is not success

        """

        flag, response = self._cvpysdk_object.make_request('GET', self._services['COMMCELL_METADATA'])

        if flag:
            if response.json():
                    commserv_metadata = {
                        'commserv_redirect_url': response.json()['redirectUrl'],
                        'commserv_certificate': response.json()['certificate']
                    }
                    return commserv_metadata
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def _get_commserv_oem_id(self):
        """Loads the commserve OEM ID and returns it

            Returns:
                commserv_oem_id (int) : returns a int representing the commserv OEM ID

            Raises:
                SDKException:
                    if failed to get commserv details
                    if response is not success
        """

        flag, response = self._cvpysdk_object.make_request('GET', self._services['GET_OEM_ID'])

        if flag:
            if response.json():
                    return response.json()['id']
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    @property
    def operator_companies(self) -> dict[str, int]:
        """
        Returns a mapping of operator companies name: id,
        available for current logged in user to operate on
        """
        return {
            opc['providerDomainName'].lower(): opc['providerId']
            for opc in self.user_mappings.get('operatorCompanies', [])
        }

    def switch_to_company(self, company_name: str):
        """Switching to Company as Operator"""
        if company_id := self.operator_companies.get(company_name.lower()):
            self._headers['operatorCompanyId'] = str(company_id)
            self._user_org = Organization(self, organization_id=company_id)
        else:
            self._user_mappings = None # refreshing once
            if not self.operator_companies.get(company_name.lower()):
                raise SDKException(
                    'Commcell', 108, f'Company {company_name} is not available/allowed '
                                     f'to operate on by this user {self.commcell_username}.'
                                     f'Choose from list: {list(self.operator_companies)}'
                )
            else:
                self.switch_to_company(company_name)

    @property
    def operating_company(self) -> str | None:
        """
        Returns the currently operating company's name, if operating any
        """
        if operating_company_id := self._headers.get('operatorCompanyId'):
            for company_name, company_id in self.operator_companies.items():
                if str(company_id) == str(operating_company_id):
                    return company_name
            raise SDKException('Commcell', 108, f'Operating unknown company. id: {operating_company_id}')
        return None

    def reset_company(self):
        """Resets company to Commcell"""
        if 'operatorCompanyId' in self._headers:
            self._headers.pop('operatorCompanyId')
        self._user_org = None

    @contextmanager
    def as_operator_of(self, company_name):
        """
        Context manager for switching to Company as Operator and returning to previous level

        Args:
            company_name (str)  -   company name to switch to
        """
        old_headers = self._headers.copy()
        self.switch_to_company(company_name)
        try:
            yield
        finally:
            self._user_org = None
            self._headers = old_headers

    def switch_to_global(self, target_commcell=None, comet_header=False):
        """
        Switching to Global scope in Multi-commcell configuration

        Args:
            target_commcell (str)   -   target commcell name if _cn header is needed
            comet_header    (bool)  -   if Comet-Commcells header is used instead of _cn
        """
        self._headers['Cvcontext'] = 'Comet'
        target_header = '_cn' if not comet_header else 'Comet-Commcells'
        if target_commcell:
            self._headers[target_header] = target_commcell

    def is_global_scope(self):
        """
        Check if comet headers are set currently, to handle api response differently

        Returns:
            bool    -   True if comet headers are active
        """
        return self._headers.get('Cvcontext') == 'Comet'

    def reset_to_local(self):
        """Resets back to local scope if in global"""
        for header in ['Cvcontext', '_cn', 'Comet-Commcells']:
            if header in self._headers:
                del self._headers[header]

    @contextmanager
    def global_scope(self, target_commcell=None, comet_header=False):
        """
        Context manager for switching to Global scope and returning to previous scope

        Args:
            target_commcell (str)   -   target commcell name if _cn header is needed
            comet_header    (bool)  -   if Comet-Commcells header is needed instead of _cn
        """
        old_headers = self._headers.copy()
        self.switch_to_global(target_commcell, comet_header)
        try:
            yield
        finally:
            self._headers = old_headers

    @contextmanager
    def custom_headers(self, **headers):
        """
        Context manager for passing additional header

        Args:
            **headers (kwargs) -- contains each header as kwargs
        """
        old_headers = self._headers.copy()
        self._headers.update(headers)
        try:
            yield
        finally:
            self._headers = old_headers

    def passkey(self, current_password, action, new_password=None):
        """"
        Updates Passkey properties of the commcell

        Args:
            current_password (str) --  User Current Passkey to perform actions
            action (str)           --  'enable' | 'disable' | 'change passkey' | 'authorize' | 'unauthorize'
            new_password (str)     --  Resetting existing Passkey

        Raises:
            SDKException:
                if invalid action is passed as a parameter

                if request fails to update passkey properties of  an organisation

                if new password is missing while changing passkey
        """

        current_password = b64encode(current_password.encode()).decode()
        commcell_organization_id = 0
        req_url = self._services['COMPANY_PASSKEY'] % commcell_organization_id

        if action.lower() == 'enable':
            req_json = {
            "newPasskey": current_password,
            "confirmPasskey": current_password,
            "passkeyOpType": "CREATE"
            }

        elif action.lower() == 'disable':
            req_json = {
                "currentPasskey": current_password,
                "confirmPasskey": current_password,
                "passkeyOpType": "DISABLE"
            }

        elif action.lower() == 'change passkey':
            if new_password:
                new_password = b64encode(new_password.encode()).decode()
                req_json = {
                    "currentPasskey": current_password,
                    "newPasskey": new_password,
                    "confirmPasskey": new_password,
                    "passkeyOpType": "EDIT"
                }
            else:
                raise SDKException('Commcell', 102, 'New password is missing in input')

        elif action.lower() in ['authorize', 'unauthorize']:
            req_json = {
                "passkey": current_password,
                "passkeySettings": {
                    "enableAuthorizeForRestore": action.lower() == 'authorize',
                    "passkeyExpirationInterval": {
                        "toTime": 1800
                    }
                }
            }
            req_url = self._services['COMPANY_AUTH_RESTORE'] % commcell_organization_id

        else:
            raise SDKException('Commcell', 102, 'Action is undefined, Invalid action passed as a parameter')

        flag, response = self._cvpysdk_object.make_request('POST', req_url, req_json)

        if flag:
            if response.json():
                if 'error' in response.json():
                    error_code = response.json()['error']['errorCode']
                    if error_code != 0:
                        error_message = response.json()['error']['errorMessage']
                        raise SDKException('Commcell', '110', 'Error: {0}'.format(error_message))
            else:
                raise SDKException('Commcell', '110')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

        self.refresh()

    def allow_users_to_enable_passkey(self, flag):
        """Enable or Disable passkey authorization for company administrators and client owners
        
        Args:
            flag (boolean)  --  Enable or Disable Passkey Authorization
            
        Raises:
            SDKException:
                if response is empty
                if response is not success
                if failed to enable or disable passkey
        """
        request_json = {
            "commCellInfo": {
                "generalInfo": {
                    "allowUsersToEnablePasskey": flag
                }
            }
        }
        flag, response = self._cvpysdk_object.make_request('PUT', self._services['SET_COMMCELL_PROPERTIES'], request_json)

        if flag:
            if response.json() and "response" in response.json():
                errorCode = response.json()['response'][0].get('errorCode')
                if errorCode != 0:
                    raise SDKException('Response', '101', 'Failed to enable passkey')
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def get_sla_configuration(self):
        """Makes a rest api call to get SLA configuration at commcell level

            Returns:
                dict   -   sla details
                example:
                    {
                        'slaDays': 7, 
                        'excludedReason': '', 
                        'useSystemDefaultSLA': False, 
                        'excludeFromSLA': False, 
                        'delayInterval': 0, 
                        'inheritedSLA': {
                            'slaDays': 0, 
                            'entityType': 0, 
                            'excludeFromSLA': False
                        }
                    }

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        request_json = {"entities": [{"entity": {"commCellId": self.commcell_id, "_type_": 1}}]}
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._services['GET_SLA'], payload=request_json
        )

        if flag:
            if response.ok and response.json():
                return response.json().get('entities', [{}])[0]
            else:
                raise SDKException('Response', '102')
        else:
            raise SDKException('Response', '101', self._update_response_(response.text))

    def get_workload_region(self):
        """Gets the workload region set at commcell level

            Returns:
                str     -   name of commcell level workload region set
                None    -   if no region set or region name not found
                example: 'US - east'
        """
        region_id = self.regions.get_region('COMMCELL', self.commcell_id, 'WORKLOAD')
        for reg_name, reg_id in self.regions.all_regions.items():
            if reg_id == region_id:
                return reg_name

    def set_workload_region(self, region_name):
        """Sets the workload region set at commcell level

            Args:
                region_name (str)   -   name of region (None to set no region)
        """
        if region_name:
            if not self.regions.has_region(region_name):
                raise SDKException('Region', '102', 'Given region not found!')
            region_id = self.regions.all_regions[region_name]
        else:
            region_id = 0
        self.regions.set_region('COMMCELL', self.commcell_id, 'WORKLOAD', region_id)

    def get_user_suggestions(self, term: str, additional_params: dict = None) -> list:
        """
        Makes api call to get user suggestions for entities
            Args:
                term               (str) - the entity name to get matched suggestions of
                additional_params (dict) - additional parameters to be passed in the url

            Returns:
                list    -   list of dicts with details of entity whose name matches for given term
                example:
                    [
                        {
                            "displayName": "",
                            "groupId": 0,
                            "umEntityType": 0,
                            "umGuid": "",
                            ...
                            "groupGuid": "...",
                            "company": {...},
                        },
                        {...},
                        {...},
                    ]

            Raises:
                SDKException:
                    if response is empty

                    if response is not success

        """
        from urllib.parse import urlencode

        if additional_params is None:
            additional_params = {}

        url_params = {
            'namePattern': term,
            'getDomainUsers': True,
            'getCommcellUsers': True,
            'getCommCellGroups': True,
            'getDomainGroups': True,
            'searchOnDisplayName': True,
            'searchOnAliasName': True,
            'searchOnSmtp': 1,
            'ignoreSmtpRule': 1,
        }
        url_params.update(additional_params)
        url_params.update({k: str(v).lower() for k, v in url_params.items() if v in [True, False]})

        api_endpoint = self._services['GET_USER_SUGGESTIONS'] + '?' + urlencode(url_params)
        flag, response = self._cvpysdk_object.make_request('GET', api_endpoint)

        if flag:
            if response.json():
                return response.json().get('users')
            else:
                raise SDKException('Response', '102')

        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def enable_limit_user_logon_attempts(self, failed_login_attempt_limit=5, failed_login_attempts_within=3600,
                                         account_lock_duration=86400, lock_duration_increment_by=3600):
        """
         Enable Limit user logon attempts feature
         Args:
             failed_login_attempt_limit             (int)   --  number of logon attempts a user is allowed
                default : 5
             failed_login_attempts_within           (int)   --  logon attempts a user is allowed within specified
                default : 3600 secs                                        numbers of secs
             account_lock_duration                  (int)   --  number of secs a locked account remains locked
                default :  86400 secs
             lock_duration_increment_by             (int)   --  increment the lock duration by specified secs
                                                                after each consecutive user account lock
                default : 3600 secs
         Raises:
            SDKException:
                if response is empty
                if response is not success
                if failed to enable limit user logon feature
        """
        req_json = {
            'failedLoginAttemptLimit': failed_login_attempt_limit,
            'failedLoginAttemptsWithin': failed_login_attempts_within,
            'accountLockDuration': account_lock_duration,
            'accountLockDurationIncrements': lock_duration_increment_by
        }
        flag, response = self._cvpysdk_object.make_request(
            'PUT', self._services['ACCOUNT_lOCK_SETTINGS'], req_json
        )
        if flag:
            if response and response.json():
                error_code = response.json().get('errorCode', -1)
                if error_code != 0:
                    error_string = response.json().get('errorMessage', '')
                    raise SDKException(
                        'Security',
                        '102',
                        'Failed to set account lock settings: "{0}"'.format(
                            error_string
                        )
                    )
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.text)
            raise SDKException('Response', '101', response_string)

    def disable_limit_user_logon_attempts(self):
        """
        Disable limit user logon attempts feature.
        Raises:
            SDKException:
                if response is empty
                if response is not success
                if failed to disable limit user logon feature
        """
        self.enable_limit_user_logon_attempts(failed_login_attempt_limit=-1,
                                              failed_login_attempts_within=-1,
                                              account_lock_duration=-1,
                                              lock_duration_increment_by=-1)

    def get_navigation_settings(self, org_id=0):
        """
        Makes a rest api call to get entire navigation preference list (for command center)

        Args:
            org_id  (int)   -   id of company to get preference list for

        Returns:
            user_nav_settings   -   dict with user role key and prefs_dict as value which has include and denied navs
            example:
                {
                  "msp_admin": {
                    "include_navs": ['gsuite','replication',....etc]
                    "denied_navs": []
                  },
                  "tenant_admin": {...},
                  "tenant_user": {...},
                  "msp_user": {...},
                  "restricted_user": {...}
                }
        """
        user_roles = {0: 'msp_admin', 1: 'tenant_admin', 2: 'tenant_user', 3: 'msp_user', 4: 'restricted_user'}
        url = self._services['NAVIGATION_SETTINGS']
        settings_type = 'globalSettings'
        if org_id:
            url += f'?organizationId={org_id}'
            settings_type = 'companySettings'

        flag, response = self._cvpysdk_object.make_request('GET', url)
        if flag:
            if response.json():
                error_response = response.json().get('error', {})
                if error_response.get('errorCode', -1) != 0:
                    error_string = error_response.get('errorMessage', '')
                    raise SDKException('Commcell', '108', error_string)

                nav_settings = {}
                for user_nav in response.json().get('navSettings', {}).get(settings_type, []):
                    nav_settings[user_roles[user_nav.get('userRole')]] = {
                        "include_navs": user_nav.get('includeNavItems', '').split(','),
                        "denied_navs": user_nav.get('deniedNavItems', '').split(',')
                    }
                return nav_settings
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.content)
            raise SDKException('Response', '101', response_string)

    def set_navigation_settings(self, nav_settings, org_id=0):
        """
        Makes a rest api call to set the navigation preference list (for command center)

        Args:
            nav_settings    (dict)  -   dict with role: navs format similar to get request return format
            example:
                {
                  "msp_admin": {
                    "include_navs": ['gsuite','replication',....etc]
                    "denied_navs": []
                  },
                  "tenant_admin": {...},
                  "tenant_user": {...},
                  "msp_user": {...},
                  "restricted_user": {...}
                }
            org_id  (int)   -   id of company to set preference list for
        """
        user_roles = {'msp_admin': 0, 'tenant_admin': 1, 'tenant_user': 2, 'msp_user': 3, 'restricted_user': 4}
        url = self._services['NAVIGATION_SETTINGS']
        settings_type = 'globalSettings'
        if org_id:
            url += f'?organizationId={org_id}'
            settings_type = 'companySettings'

        settings = []
        for role, nav_items in nav_settings.items():
            settings.append({"userRole": user_roles[role]})
            if "include_navs" in nav_items:
                settings[-1]["includeNavItems"] = ",".join(nav_items["include_navs"])
            if "denied_navs" in nav_items:
                settings[-1]["deniedNavItems"] = ",".join(nav_items["denied_navs"])

        request_json = {
            'navSettings': {
                settings_type: settings
            }
        }
        flag, response = self._cvpysdk_object.make_request('POST', url, payload=request_json)
        if flag:
            if response.json():
                if response.json().get('errorCode', -1) != 0:
                    error_string = response.json().get('errorMessage', '')
                    raise SDKException('Commcell', '108', error_string)
            else:
                raise SDKException('Response', '102')
        else:
            response_string = self._update_response_(response.content)
            raise SDKException('Response', '101', response_string)

    @property
    def cost_assessment(self):
        """Returns the instance of Cost assessment class."""
        try:
            if self._cost_assessment is None:
                self._cost_assessment = CostAssessment(self)

            return self._cost_assessment
        except AttributeError:
            return USER_LOGGED_OUT_MESSAGE

    def get_environment_tile_details(self, comet_flag: bool = False) -> dict[str, dict[str, int]]:
        """
        Retrieves environment tile details like counts of file servers, VMs, laptops, and users
        for the Commcell.

        Args:
            comet_flag (bool): If True, fetches details for each service Commcell.

        Returns:
            dict: A dictionary containing the environment tile details.

            Example (when comet_flag is True):
            {
                'commcell1': {
                    'fileServerCount': 5,
                    'laptopCount': 1,
                    'vmCount': 9,
                    'usersCount': 48
                },
                'commcell2': {
                    'fileServerCount': 3,
                    'laptopCount': 0,
                    'vmCount': 2,
                    'usersCount': 382
                },
                ...
                'totalCount': {
                    'fileServerCount': 56,
                    'laptopCount': 2,
                    'vmCount': 453,
                    'usersCount': 2415
                }
            }

            Example (when comet_flag is False):
            {
                'fileServerCount': 56,
                'laptopCount': 2,
                'vmCount': 453,
                'usersCount': 2415
            }
        """
        if comet_flag:
            self.switch_to_global()

        # Fetch environment tile counts - fileserver,vm,laptop
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._services['DASHBOARD_ENVIRONMENT_TILE']
        )
        if not flag:
            raise SDKException('Response', '101', self._update_response_(response.text))

        resp_json = response.json()
        if not resp_json:
            raise SDKException('Response', '102')

        # Fetch environment tile counts - users
        flag_1, response_1 = self._cvpysdk_object.make_request(
            'GET', self._services['DASHBOARD_ENVIRONMENT_TILE_USERS']
        )
        if not flag_1:
            raise SDKException('Response', '101', self._update_response_(response_1.text))

        resp_json_1 = response_1.json()
        if not resp_json_1:
            raise SDKException('Response', '102')

        environment_tile_dict = {}
        main_keys = ['fileServerCount', 'laptopCount', 'vmCount']

        if comet_flag:
            commcell_data = {}

            # Populate fileServerCount, laptopCount, vmCount
            for tile in resp_json.get('cometClientCount', []):
                commcell_name = tile.get('commcell',{}).get('commCellName','')
                if not commcell_name:
                    continue
                commcell_data.setdefault(commcell_name, {})
                for key in main_keys:
                    commcell_data[commcell_name][key] = tile.get(key, 0)

            # Populate usersCount
            for item in resp_json_1.get('commcellWiseAggregation', []):
                commcell_name = item.get('commcellName', '')
                if not commcell_name:
                    continue
                func_value = item.get('aggregation', [{}])[0].get('funcValue', 0)
                commcell_data.setdefault(commcell_name, {})
                commcell_data[commcell_name]['usersCount'] = int(func_value)

            # Add totalCount as a separate key
            commcell_data['totalCount'] = {
                key: resp_json.get('totalCount', {}).get(key, 0) if key != 'usersCount' else
                     int(resp_json_1.get('aggregation', [{}])[0].get('funcValue', 0))
                for key in ['fileServerCount', 'laptopCount', 'vmCount', 'usersCount']
            }

            environment_tile_dict = commcell_data
        else:
            for key in main_keys:
                environment_tile_dict[key] = resp_json.get(key, 0)

            environment_tile_dict['usersCount'] = int(
                resp_json_1.get('aggregation', [{}])[0].get('funcValue', 0)
            )
        if comet_flag:
            self.reset_to_local()
        return environment_tile_dict