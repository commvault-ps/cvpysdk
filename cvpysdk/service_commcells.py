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
Main file for performing service commcell related operations

ServiceCommcells: Class for managing Service Commcells registered to this router commcell
    Methods:
        add()                       --  registers a service commcell
        has_service_commcell()      --  checks if a service commcell with the given name exists
        delete()                    --  deletes a service commcell with the given name
        get()                       --  gets the service commcell object for the given service commcell
        refresh()                   --  refreshes the cached service commcells information
        get_service_rules()         --  gets the service rules for this commcell to be shared with router commcell

    Properties:
        associations                --  returns an Associations object for managing associations of service commcells
        all_service_commcells       --  returns all service commcell details
        global_mongo_status         --  returns the global mongoDB status/health for each registered service commcell
        commcells_for_user          --  returns the list of accessible commcells to currently logged user
        commcells_for_switching     --  returns the commcell details for all switchable commcells


ServiceCommcell: Class for performing operations on a single service commcell
    Methods:
        update()                    --  updates the properties of the service commcell
        reregister()                --  reregisters this commcell with the provided username and password
        refresh_sync()              --  refreshes the service commcell's properties synced with the router commcell
        refresh()                   --  refreshes the cached properties of the service commcell obj

    Properties:
        props                       --  returns the properties of the service commcell
        commcell_id                 --  returns the commcell ID of the service commcell
        cs_guid                     --  returns the csGUID of the service commcell
        client_id                   --  returns the client ID of the service commcell
        client_name                 --  returns the client name of the service commcell
        interface_name              --  returns the interface name of the service commcell
        display_name                --  returns the display name of the service commcell
        webconsole_url              --  returns the webconsole URL of the service commcell
        service_pack_info           --  returns the service pack information of the service commcell
        sync_status                 --  returns the sync status of the service commcell
        role_string                 --  returns the role string of the service commcell
        details                     --  returns detailed properties of the service commcell
        associations                --  Associations object for managing associations of this service commcell


Associations:  Class for managing associations of service commcell(s)
    Methods:
        get()                       --  gets an entity's association details
        add()                       --  adds entity association to the specified service commcell
        delete()                    --  deletes entity associations from the specified service commcell(s)

    Properties:
        all_associations            --  returns all associations of service commcells
"""

from __future__ import absolute_import
from __future__ import unicode_literals

from base64 import b64encode
from typing import Any, TYPE_CHECKING

from .exception import SDKException
if TYPE_CHECKING:
    from .commcell import Commcell


class ServiceCommcells:
    """
    Class for performing service commcell operations
    """
    def __init__(self, commcell_object: 'Commcell'):
        """Initialise the Activity control class instance.

            Args:
                commcell_object (Commcell) - instance of the Commcell class

            Returns:
                object - instance of the ServiceCommcells class
        """
        self._commcell = commcell_object
        self.associations = Associations(self._commcell)
        self._service_commcells = None
        self._global_mongo_status = None
        self._commcells_for_user = None
        self._commcells_for_switching = None

    def __repr__(self):
        """String representation of the instance of this class."""
        return f'ServiceCommcells class instance for commcell: {self._commcell.webconsole_hostname}'

    def __getitem__(self, item) -> 'ServiceCommcell':
        return self.get(item)

    def refresh(self):
        """
        Refreshes the cached service commcells information
        """
        self._service_commcells = None
        self._global_mongo_status = None
        self._commcells_for_user = None
        self._commcells_for_switching = None
        self.associations.refresh()

    def _get_commcells_for_switching(self) -> dict[str, Any]:
        """
        returns the commcell details for all switchable commcells

        Returns:
            dict - dict with details on accessible commcells

            Example:
            {
                'serviceCommcell': [
                    {'webUrl': '...', 'commcellRole': ..., 'commcellHostname': '...'},
                    {...}, {...},
                ]
                'IDPCommcell': {...},
                'routerCommcell': [{...}]
            }

        Raises:
            SDKException:
                if response is empty

                if response is not success
        """
        return self._commcell.wrap_request('GET', 'MULTI_COMMCELL_SWITCHER')

    def _get_commcells_for_user(self) -> list[dict[str, Any]]:
        """
        Returns the list of accessible commcells to currently logged user

        Returns:
            list - consists list of dicts with info about accessible commcells

                [
                    {'redirectUrl': '', 'commcellName': '', 'commcellType': ''},
                    {...},
                    ...
                ]
        Raises:
            SDKException:
                if response is empty

                if response is not success
        """
        return self._commcell.wrap_request('GET', 'MCC_FOR_USER').get('AvailableRedirects', [])

    def _get_global_mongodb_status(self) -> dict:
        """
        returns the Global mongoDB status/health for each registered service commcell

        Returns:
            dict - dict with global mongo status details

        Raises:
            SDKException:
                if response is empty

                if response is not success
        """
        with self._commcell.global_scope():
            response = self._commcell.wrap_request('GET', 'GLOBAL_MONGODB_STATUS')
        return {
            cs_prop['commcellName']: cs_prop for cs_prop in response
        }

    def _get_service_commcells(self) -> dict[str, dict[str, Any]]:
        """
        Gets the registered routing commcells

        Returns:
            dict - consists of all registered routing commcells
                {
                    "commcell_name1": {
                        'displayName': ...,
                        'multiCommcellType': ...,
                        'statusDetail': ...,
                        'disableAggregation': ...,
                        'lastSyncWithIDP': ...,
                        'activeManagementStatus': ...
                        ....
                    },
                    "commcell_name2:: {...}
                }
        Raises:
            SDKException:
                if response is empty

                if response is not success
        """
        resp = self._commcell.wrap_request(
            'GET', 'SERVICE_COMMCELLS', empty_check=False
        )
        return {
            commcell['commCell']['commCellName']: commcell
            for commcell in resp.get('commcellsList', [])
        }

    def add(self, cc_url: str, username: str, password: str, **kwargs):
        """
        Registers a service commcell

        Args:

            cc_url (str)                    --  command center URL of the service commcell to register

            username   (str)                --  username of the user who has administrative
                                                rights on a commcell

            password  (str)                 --  password of the user specified

            kwargs: any other payload parameters to pass

        Raises:

            SDKException:

                if the registration fails
                if response is empty
                if there is no response

        """
        cc_url = cc_url.lower()
        if not cc_url.endswith("/commandcenter"):
            cc_url = cc_url.rstrip('/')
            cc_url += '/commandcenter'
        if not cc_url.startswith("https://") or cc_url.startswith("http://"):
            cc_url = "http://" + cc_url

        payload = {
            "serviceCommcelWebconsoleUrl": cc_url,
            "username": username,
            "password": b64encode(password.encode()).decode(),
            "isIDPCommcell": False,
            "userOrGroup": [],
        } | kwargs

        self._commcell.wrap_request(
            'POST', 'SERVICE_REGISTER', req_kwargs={'payload': payload},
            sdk_exception=('ServiceCommcells', '102'),
        )
        self.refresh()

    def has_service_commcell(self, commcell_name: str) -> bool:
        """
        Checks if the service commcell with the given name exists

        Args:
            commcell_name (str) - commserv name of the service commcell

        Returns:
            bool - True if service commcell exists, False otherwise
        """
        return commcell_name in self.all_service_commcells

    def delete(self, commcell_name: str, force: bool = False):
        """
        Deletes the service commcell with the given name

        Args:
            commcell_name (str) - commserv name of the service commcell
            force (bool) - if True, forces the deletion without confirmation
        """
        payload = {
          "commcell": {
            "commCell": {
              "commCellId": self[commcell_name].commcell_id,
              "csGUID": self[commcell_name].cs_guid,
            },
            "ccClientId": self[commcell_name].client_id,
            "ccClientName": self[commcell_name].client_name,
            "interfaceName": self[commcell_name].interface_name
          },
          "forceUnregister": force
        }

        self._commcell.wrap_request(
            'POST', 'UNREGISTRATION',
            req_kwargs={'payload': payload},
            sdk_exception=('ServiceCommcells', '103')
        )
        self.refresh()

    def get(self, commcell_name: str) -> 'ServiceCommcell':
        """
        Gets the service commcell object for the given service commcell

        Args:
            commcell_name (str) - commserv name of the service commcell
        """
        if commcell_name in self.all_service_commcells:
            return ServiceCommcell(self._commcell, commcell_name)
        else:
            raise SDKException('ServiceCommcells', '102', f'No service commcell found with name: {commcell_name}')

    @property
    def all_service_commcells(self) -> dict[str, Any]:
        """
        Returns all service commcell details

        Example:
        {
            "commcell_name1": {
                'displayName': ...,
                'multiCommcellType': ...,
                'statusDetail': ...,
                'disableAggregation': ...,
                'lastSyncWithIDP': ...,
                'activeManagementStatus': ...
                ....
            },
            "commcell_name2:: {...}
        }
        """
        if self._service_commcells is None:
            self._service_commcells = self._get_service_commcells()
        return self._service_commcells

    @property
    def global_mongo_status(self) -> dict:
        """
        Returns the global mongoDB status/health for each registered service commcell
        """
        if self._global_mongo_status is None:
            self._global_mongo_status = self._get_global_mongodb_status()
        return self._global_mongo_status

    @property
    def commcells_for_user(self) -> list[dict[str, Any]]:
        """
        Returns the list of accessible commcells to currently logged user

        Returns:
            list - consisting of all accessible commcells to the user
                [
                    {'redirectUrl': '', 'commcellName': '', 'commcellType': ''},
                    {...},
                    ...
                ]
        """
        if self._commcells_for_user is None:
            self._commcells_for_user = self._get_commcells_for_user()
        return self._commcells_for_user

    @property
    def commcells_for_switching(self) -> dict[str, Any]:
        """
        Returns the commcell details for all switchable commcells

        Returns:
            dict - dict with details on service, IDP and router commcells
            {
                'serviceCommcell': [
                    {'webUrl': '...', 'commcellRole': ..., 'commcellHostname': '...'},
                    {...}, {...},
                ]
                'IDPCommcell': {...},
                'routerCommcell': [{...}]
            }
        """
        if self._commcells_for_switching is None:
            self._commcells_for_switching = self._get_commcells_for_switching()
        return self._commcells_for_switching


class ServiceCommcell:
    """
    Class for performing operations on a service commcell
    """
    def __init__(self, commcell_object: 'Commcell', commcell_name: str):
        """
        Initialise the ServiceCommcell class instance.

        Args:
            commcell_object (Commcell)  - instance of the Commcell class
            commcell_name (str)         - commserve name of the service commcell

        Returns:
            object - instance of the ServiceCommcell class
        """
        self._commcell = commcell_object
        self.commcell_name = commcell_name
        self.associations = Associations(self._commcell, commcell_name)
        self._props = None
        self._details = None
        self._mongo_status = None

    def __repr__(self):
        """String representation of the instance of this class."""
        return f'service commcell {self.commcell_name} of router commcell: {self._commcell.webconsole_hostname}'

    def refresh(self):
        """
        Refreshes the properties of the service commcell
        """
        self._props = None
        self._details = None
        self._mongo_status = None
        self._commcell.service_commcells.refresh()
        self.associations.refresh()

    def _get_details(self) -> dict:
        """
        Gets the detailed props of the service commcell, using properties API

        Returns:
            dict - detailed properties of the service commcell
            {
                'associations': [...],
                'properties': {
                    'webServiceUrl': ...,
                    'commCellName': ...,
                    'commcellNumber': ...,
                    'servicePackInfo': ...,
                    ...
                }
            }
        """
        return self._commcell.wrap_request(
            'GET', 'SERVICE_PROPS',
            req_kwargs={'params': {'commcellId': self.commcell_id}}
        )

    def update(self, properties: dict):
        """
        Updates the properties of the service commcell

        Args:
            properties      (dict)  --  dict with properties to be updated
                example: {'displayName': '...', 'webconsoleUrl': '...'}
        """
        payload = {
            "properties": {'csGUID': self.cs_guid.upper()} | properties
        }
        response = self._commcell.wrap_request(
            'POST', 'SERVICE_PROPS',
            req_kwargs={'payload': payload},
            sdk_exception=('ServiceCommcell', '106'),
            return_resp=True
        )
        self.refresh()
        return response.headers.get("comet-response")

    def reregister(self, username: str, password: str):
        """
        Reregisters this commcell with the provided username and password

        Args:
            username        (str)           --  username of the user who has administrative
                                                rights on a commcell

            password        (str)           --  password of the user
        """
        payload = {
            "username": username,
            "password": b64encode(password.encode()).decode(),
        }
        self._commcell.wrap_request(
            'POST', 'SERVICE_REREGISTER', (self.commcell_id,),
            req_kwargs={'payload': payload},
            sdk_exception=('ServiceCommcell', '107'),
        )
        self.refresh()

    def refresh_sync(self):
        """
        Refresh the service commcell's properties synced with the router commcell

        Raises:

            if sync fails
            if the response is empty
            if there is no response

        """
        payload = {'commcellId': self.commcell_id}
        self._commcell.wrap_request(
            'GET', 'SYNC_SERVICE_COMMCELL', (self.commcell_id,),
            req_kwargs={'params': payload},
            sdk_exception=('ServiceCommcell', '108'),
            error_check=True
        )
        self.refresh()

    @property
    def props(self) -> dict:
        """
        Returns the properties of the service commcell
        """
        if self._props is None:
            self._props = self._commcell.service_commcells.all_service_commcells.get(self.commcell_name)
            if not self._props:
                raise SDKException(
                    'ServiceCommcells', '105', f'No props returned for: {self.commcell_name}'
                )
        return self._props

    @property
    def commcell_id(self) -> int:
        """
        Returns the commcell ID of the service commcell
        """
        return self.props.get('commCell', {}).get('commCellId')

    @property
    def cs_guid(self) -> str:
        """
        Returns the csGUID of the service commcell
        """
        return self.props.get('commCell', {}).get('csGUID')

    @property
    def client_id(self) -> int:
        """
        Returns the client ID of the service commcell
        """
        return self.props.get('ccClientId')

    @property
    def client_name(self) -> str:
        """
        Returns the client name of the service commcell
        """
        return self.props.get('ccClientName')

    @property
    def interface_name(self) -> str:
        """
        Returns the interface name of the service commcell
        """
        return self.props.get('interfaceName')

    @property
    def display_name(self) -> str:
        """
        Returns the display name of the service commcell
        """
        return self.props.get('displayName')

    @display_name.setter
    def display_name(self, value: str):
        """
        Sets the display name of the service commcell

        Args:
            value (str) - new display name to set
        """
        self.update({'displayName': value})

    @property
    def webconsole_url(self) -> str:
        """
        Returns the webconsole URL of the service commcell
        """
        return self.props.get('webconsoleUrl')

    @property
    def service_pack_info(self) -> str:
        """
        Returns the service pack information of the service commcell
        """
        return self.props.get('servicePackInfo')

    @property
    def sync_status(self) -> bool:
        """
        Returns the sync status of the service commcell
        """
        return self.props.get('syncStatus', {}).get('status') == 1

    @property
    def role_string(self) -> str:
        """
        Returns the role string of the service commcell
        """
        return self.props.get('commcellRoleString', '')

    @property
    def details(self) -> dict:
        """
        Returns the detailed properties of the service commcell
        """
        if self._details is None:
            self._details = self._get_details()
        return self._details

    @property
    def mongo_status(self) -> dict:
        """
        Returns the mongoDB status/health of the service commcell

        Returns:
            dict - consisting of mongoDB status details
        """
        if self._mongo_status is None:
            self._mongo_status = self._commcell.service_commcells.global_mongo_status.get(self.commcell_name)
        return self._mongo_status


class Associations:
    """
    Class for managing associations of service commcells
    """
    entity_payload_map = {
        'User': lambda entity: {
            'userOrGroup': {
                'userId': int(entity.user_id),
                'userName': entity.user_name,
                '_type_': 13
            }
        },
        'UserGroup': lambda entity: {
            'userOrGroup': {
                'userGroupId': int(entity.user_group_id),
                'userGroupName': entity.user_group_name,
                '_type_': 15
            }
        },
        'Domain': lambda entity: {
            'providerType': 2,
            'userOrGroup': {
                'providerId': int(entity.domain_id),
                'providerDomainName': entity.domain_name,
                '_type_': 61
            }
        },
        'Organization': lambda entity: {
            'providerType': 5,  # todo: this may be 15 or 5 depending on something
            'userOrGroup': {
                'providerId': int(entity.organization_id),
                'providerDomainName': entity.domain_name,
                '_type_': 61,
                'GUID': entity.provider_guid,
                'entityInfo': {
                    "multiCommcellName": entity._commcell_object.commserv_name
                }
            }
        }
    }

    @staticmethod
    def lookup_entity_payload(entity: Any) -> dict:
        """
        Returns the payload for the given entity type

        Args:
            entity (object) - object of User, UserGroup, Domain or Organization class
                              or Any Derived class of the Above

        Returns:
            dict - payload for the entity
        """
        for cls in type(entity).__mro__:
            name = cls.__name__
            if name in Associations.entity_payload_map:
                return Associations.entity_payload_map[name](entity)
        raise SDKException('ServiceCommcells', '101', f'Invalid entity type: {type(entity)} : {entity}')

    def __init__(self, commcell_object, filter_commcell: str = None):
        """
        Initialise the Associations class instance.

        Args:
            commcell_object (Commcell)   - instance of the Commcell class
            filter_commcell (str)        - commserv name of the service commcell to filter associations
        """
        self._commcell = commcell_object
        self._filter_commcell = filter_commcell
        self._associations = None

    def __repr__(self):
        """String representation of the instance of this class."""
        if not self._filter_commcell:
            return f'service commcell associations from router: {self._commcell.webconsole_hostname}'
        else:
            return (f'associations of service commcell: {self._filter_commcell} '
                    f'from router: {self._commcell.webconsole_hostname}')

    def refresh(self):
        """
        Refreshes the cached associations information
        """
        self._associations = None

    def _associations_api_call(self, method: str, exc_code: int, payload: dict = None, **kwargs) -> dict:
        response_json = self._commcell.wrap_request(
            method, 'SERVICE_COMMCELL_ASSOC',
            req_kwargs={'payload': payload} if payload else {},
            sdk_exception=('ServiceCommcells', exc_code)
        )
        if kwargs.get('include_warning'):
            warning_code = response_json.get('warningCode', 0)
            if warning_code != 0:
                error_string = response_json.get('warningMessage')
                raise SDKException('ServiceCommcells', exc_code, error_string)
        return response_json

    def _form_assoc_dict(self, entity, commcell) -> dict:
        """
        prepares the entity json for adding commcell associations

        Args:
            entity (object)    --  object of User, UserGroup, Domain or Organization class
            commcell (str)     --  commserv name of the service commcell

        Returns:
            dict - entity json for adding commcell associations
        """
        if not isinstance(commcell, str):
            raise SDKException('ServiceCommcells', '101', 'commcell must be a string')
        return {
            "entity": {
                "entityType": 194,
                "entityName": commcell,
                "_type_": 150,
                "entityId": self._commcell.service_commcells[commcell].commcell_id
            },
            **self.lookup_entity_payload(entity)
        }

    def _form_assoc_list(self, entities, commcells) -> list[dict]:
        """
        prepares the entity json for adding commcell associations

        Args:
            entities (object or list)    --  object(s) of User, UserGroup, Domain or Organization class
            commcells (str or list)      --  commserv name(s) of the service commcell(s)

        Returns:
            dict - entity json for adding commcell associations
        """
        if not isinstance(entities, list):
            entities = [entities]
        if not isinstance(commcells, list):
            commcells = [commcells]
        return [
            self._form_assoc_dict(entity, commcell) for entity in entities for commcell in commcells
        ]

    def get(self, entity, commcell=None) -> list[dict]:
        """
        Gets an entity's association details for every commcell it is associated to

        Args:
            entity  (object)     --      can be object of User,UserGroup,Domain and Organization Class
                                         or a string of the entity name
                                         or a list of the above

            commcell (str or list) --   commserv name(s) of the service commcell(s) to filter associations

        Returns:
            list - list of dicts, each dict containing details of the entity's association with a service commcell

            Example:
                [
                    {
                        "userOrGroup": {
                            "userId": ,
                            "GUID": ,
                            "userName": ,
                            "_type_": ,
                        },
                        "entity": {
                            "entityType": ,
                            "entityName": ,
                            "entityId": ,
                            "_type_": ,
                            "flags": ,
                        },
                        "properties": ,
                    },
                    {
                        "userOrGroup": {...},
                        "entity": {...},
                        "properties": {...},
                    },
                    {
                        "userOrGroup": {...},
                        "entity": {...},
                        "properties": {...},
                    }
                ]

        """
        commcell = commcell or self._filter_commcell
        if isinstance(commcell, str):
            commcell = [commcell]
        if isinstance(entity, list):
            return [
                assoc for each_entity in entity for assoc in self.get(each_entity)
            ]

        if isinstance(entity, str):
            assoc_match = lambda assoc_dict: entity.lower() in [
                assoc_dict['userOrGroup'].get('userName', '').lower(),
                assoc_dict['userOrGroup'].get('userGroupName', '').lower(),
                assoc_dict['userOrGroup'].get('providerDomainName', '').lower()
            ]
        else:
            catch_assoc_dict = self.lookup_entity_payload(entity)
            assoc_match = lambda assoc_dict: (
                set(assoc_dict['userOrGroup'].items()).issuperset(
                    set(catch_assoc_dict['userOrGroup'].items())
                )
            )
        entity_assocs = [
            assoc for assoc in self.all_associations if assoc_match(assoc)
        ]
        if commcell:
            entity_assocs = [
                assoc for assoc in entity_assocs if assoc['entity']['entityName'] in commcell
            ]
        return entity_assocs

    def add(self, entity, commcell=None, **kwargs):
        """
        Adds an association for the given entity to the specified service commcell

        Args:
            entity (object)     --  object(s) of User, UserGroup, Domain or Organization class
            commcell (str)      --  commserv name of the service commcell(s)
            kwargs:
                include_warning (bool) - if True, will raise exception for warning messages as well

        Raises:
            SDKException:
                if the entity is not valid
                if the response is empty
                if the response is not success
        """
        commcell = commcell or self._filter_commcell
        self._associations_api_call(
            'POST', 110,
            {
                "associations": self._form_assoc_list(entity, commcell),
                "associationsOperationType": 2
            },
            **kwargs
        )
        self.refresh()

    def delete(self, entity, commcell=None, **kwargs):
        """
        Deletes an association for the given entity from the specified service commcell(s)
        """
        commcell = commcell or self._filter_commcell
        if assocs_to_delete := self.get(entity, commcell):
            self._associations_api_call(
                'POST', 111,
                {
                    "associations": assocs_to_delete,
                    "associationsOperationType": 3
                },
                **kwargs
            )
            self.refresh()

    @property
    def all_associations(self) -> list[dict]:
        """
        Returns all associations of service commcells

        Returns:
            list - consisting of all entities associated with service commcells
        """
        if self._associations is None:
            all_assocs = self._associations_api_call('GET', 109).get('associations', [])
            if self._filter_commcell:
                all_assocs = [
                    assoc for assoc in all_assocs if assoc['entity']['entityName'] == self._filter_commcell
                ]
            self._associations = all_assocs
        return self._associations
