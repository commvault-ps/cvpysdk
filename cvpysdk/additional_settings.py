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
Main file for performing additional setting operations

AdditionalSettings is the only class defined in this file.

AdditionalSettings: Class for managing Additional Settings on various entities within the commcell.

AdditionalSettings:
    __init__                    --  initialise the AdditionalSettings class instance

    add_additional_setting      --  Adds an additional setting

    edit_additional_setting     --  Edits an additional setting

    delete_additional_setting   --  Deletes an additional setting

    get_additional_settings     --  Returns all the additional settings for the entity

    additional_settings         --  Cached property to access all additional settings

"""

from __future__ import absolute_import
from __future__ import unicode_literals

from .exception import SDKException


class AdditionalSettings(object):
    """Class for performing activity control operations."""
    entity_type_ids_map = {
        'Client': 3,
        'ClientGroup': 28,
        'Organization': 189,
        'User': 13,
        'UserGroup': 15,
    }
    entity_id_prop = {
        'Client': 'client_id',
        'ClientGroup': 'clientgroup_id',
        'Organization': 'organization_id',
        'User': 'user_id',
        'UserGroup': 'user_group_id',
    }

    @staticmethod
    def lookup_entity_type(entity) -> str | None:
        for cls in type(entity).__mro__:
            name = cls.__name__
            if name in AdditionalSettings.entity_id_prop:
                return name
        return None

    def __init__(self, entity_object):
        """Initialise the Activity control class instance.

            Args:
                entity_object (object)  --  instance of the entity object

            Returns:
                object - instance of the AdditionalSettings class
        """

        self._entity_object = entity_object
        entity_class = self.lookup_entity_type(entity_object)
        if not entity_class:
            raise SDKException('AdditionalSettings', '101',
                               f'Unsupported entity of type: {type(entity_object)}')

        self._entity_type_id = self.entity_type_ids_map[entity_class]
        self._entity_id = getattr(self._entity_object, self.entity_id_prop.get(entity_class))

        self._additional_settings = {}

        self._commcell_object = self._entity_object._commcell_object

    def __repr__(self):
        """String representation of the instance of this class."""
        return f'AdditionalSettings class instance for entity: {self._entity_object}'

    def _v4_workload_settings_api_caller(self, request_type, other_props=None):
        other_props = other_props or {}
        def api_caller(key_name, category, data_type, value, comment, enabled):
            properties_dict = {
                "additionalSettings": [
                    {
                        "entityInfo": {
                            "entityId": int(self._entity_id),
                            "entityType": self._entity_type_id,
                            "_type_": self._entity_type_id
                        },
                        "registryKeys": [
                            {
                                "relativepath": category,
                                "keyName": key_name,
                                "type": data_type,
                                "value": value,
                                "enabled": int(enabled),
                                "comment": comment
                            } | other_props
                        ]
                    }
                ]
            }
            self._commcell_object.wrap_request(
                request_type, 'SET_ADDITIONAL_SETTINGS',
                req_kwargs={'payload': properties_dict},
                sdk_exception=('AdditionalSettings', '102')
            )
            self.refresh()
        return api_caller

    def add_additional_setting(
            self, key_name, category, data_type, value, comment="Added using automation", enabled: bool = True):
        """
        Adds additional settings on entity

        Args:
            key_name (str)          : Name of the key to be added
            category (str)          : Category under which the key should be added
            data_type (str)         : Data type of the additional setting ('BOOLEAN', 'INTEGER', 'STRING', etc.)
            value (str)             : Value to be set for the key
            comment (str, optional) : Comment for the key. Defaults to "Added using automation".
            enabled (bool, optional): Whether the setting is enabled. Defaults to True.
        """
        self._v4_workload_settings_api_caller('POST')(key_name, category, data_type, value, comment, enabled)

    def edit_additional_setting(self, key_name, value=None, comment=None, enabled=None):
        """
        Edits an additional setting for the entity

        Args:
            key_name (str)          : Name of the key to be edited
            value (str, optional)   : New value for the key
            comment (str, optional) : New comment for the key
            enabled (bool, optional) : Whether the setting is enabled. Defaults to None.
        """
        key_details = self.all_additional_settings.get(key_name)
        if not key_details:
            raise SDKException('AdditionalSettings', '102',
                               f'Key {key_name} does not exist on entity: {self._entity_object}')
        category, data_type = key_details[1:3]
        value = value or key_details[3]
        comment = comment or key_details[4]
        enabled = enabled if enabled is not None else key_details[5]
        self._v4_workload_settings_api_caller('PUT')(key_name, category, data_type, value, comment, enabled)

    def delete_additional_setting(self, key_name):
        """
        Deletes an additional setting from the entity

        Args:
            key_name (str)  : Name of the key to be deleted
        """
        key_details = self.all_additional_settings.get(key_name)
        if not key_details:
            return
        self._v4_workload_settings_api_caller('PUT', {'deleted': 1})(*key_details)

    def get_additional_settings(self):
        """
        Returns all the additional settings for the entity
        """
        response_json = self._commcell_object.wrap_request(
            'GET', 'GET_ADDITIONAL_SETTINGS', (self._entity_type_id, self._entity_id)
        )
        return {
            setting['name']: (
                setting['name'],
                setting['category'],
                setting['type'],
                setting.get('values', [{}])[0].get('value', ''),
                setting.get('comment', ''),
                bool(setting.get('enabled', True))
            )
            for setting in response_json.get('additionalSettings', [])
        }

    @property
    def all_additional_settings(self):
        """
        Returns the additional settings for the entity

        Returns:
            dict: A dictionary containing additional settings
        """
        if not self._additional_settings:
            self._additional_settings = self.get_additional_settings()
        return self._additional_settings

    def refresh(self):
        """Refreshes the additional settings for the entity."""
        self._additional_settings = {}