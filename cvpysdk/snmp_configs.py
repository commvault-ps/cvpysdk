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

""" File for managing SNMP Configurations in Commcell """
import base64
from .exception import SDKException


class SNMPConfigurations:
    """ Class for managing SNMP Configurations in Commcell """

    def __init__(self, commcell_object):
        """ Initialize the SNMPConfiguration class

        Args:
            commcell_object (object): Instance of the Commcell class
        """
        self._commcell_object = commcell_object
        self._cvpysdk_object = commcell_object._cvpysdk_object
        self._update_response_ = commcell_object._update_response_
        self._SNMP = self._commcell_object._services['SNMP']
        self._SNMP_CONFIG = self._commcell_object._services['SNMP_CONFIG']
        self._configs = None
        self.encrypt_algo_ids = {
            "HMAC_MD5": 1,
            "HMAC_SHA": 2,
            "HMAC128_SHA224": 3,
            "HMAC192_SHA256": 4,
            "HMAC256_SHA384": 5,
            "HMAC384_SHA512": 6
        }
        self.privacy_algo_ids = {
            "None": 0,
            "CBC_DES": 1,
            "CFB128_AES128": 2,
            "CBC_AES128": 3
        }
        self.encrypt_algo_names = {v: k for k, v in self.encrypt_algo_ids.items()}
        self.privacy_algo_names = {v: k for k, v in self.privacy_algo_ids.items()}

    def refresh(self):
        self._configs = None

    def _get_all_configs(self) -> dict:
        """ Returns all the SNMP configurations in the Commcell

        Returns:
            dict: Dictionary of all SNMP configurations
        """
        flag, response = self._cvpysdk_object.make_request(
            'GET', self._SNMP_CONFIG
        )
        if flag:
            if response and "snmv3InfoList" in response.json():
                return {
                    config["hostName"]: {
                        'privacy_algorithm':  self.privacy_algo_names[config["privacyAlgorithm"]],
                        'authentication_algorithm': self.encrypt_algo_names[config["encryptAlgorithm"]],
                        'id': config["id"],
                        'user_name': config["userAccount"]["userName"],
                    }
                    for config in response.json()["snmv3InfoList"]
                }
            else:
                return {}
        response_string = self._update_response_(response.content)
        raise SDKException('Response', '101', response_string)

    @property
    def all_configs(self) -> dict:
        """ Returns all the SNMP configurations in the Commcell

        Returns:
            list: List of all SNMP configurations
        """
        if self._configs is None:
            self._configs = self._get_all_configs()
        return self._configs

    def _update_config(self, optype: int, config_hostname: str, username: str, password: str= '', **kwargs) -> None:
        """
        Updates the SNMP configurations in the Commcell

        Args:
            optype (int): Operation type for the SNMP configuration (1 - Add, 2 - Delete, 3 - Update)
            config_hostname (str): Host name of the SNMP configuration
            username (str): Username for the SNMP configuration
            password (str): Password for the SNMP configuration
            kwargs:
                authentication_algorithm (str): Authentication algorithm for the SNMP configuration
                                                default: HMAC_MD5
                privacy_algorithm (str): Privacy algorithm for the SNMP configuration
                                         default: None
                privacy_password (str): Privacy password for the SNMP configuration
        """
        payload = {
            "snmv3ConfigOperationType": optype,
            "snmv3Info": {
                "hostName": config_hostname,
                "encryptAlgorithm": self.encrypt_algo_ids[kwargs.get("authentication_algorithm", "HMAC_MD5")],
                "privacyAlgorithm": 0,
                "privacyCredentials": False,
                "userAccount": {
                    "userName": username
                }
            }
        }
        if optype == 3:
            payload["snmv3Info"]["id"] = kwargs.get('id')
        if password:
            payload["snmv3Info"]["userAccount"]["password"] = base64.b64encode(password.encode()).decode()
        if (priv_algo := kwargs.get("privacy_algorithm")) not in ["None", None]:
            payload["snmv3Info"]["privacyCredentials"] = True
            payload["snmv3Info"]["privacyAlgorithm"] = self.privacy_algo_ids[priv_algo]
            if priv_pass := kwargs.get("privacy_password"):
                payload["snmv3Info"]["privacyPassword"] = base64.b64encode(priv_pass.encode()).decode()
        flag, response = self._cvpysdk_object.make_request(
            'POST', self._SNMP_CONFIG, payload
        )
        if flag:
            if response.json():
                self.refresh()
                return
            else:
                raise SDKException('Commcell', '101', f'Failed to update SNMP configuration: {config_hostname}')
        response_string = self._update_response_(response.content)
        raise SDKException('Response', '101', response_string)

    def add(self, config_hostname: str, username: str, password: str, **kwargs) -> None:
        """ Adds a new SNMP configuration to the Commcell

        Args:
            config_hostname (str): Host name of the SNMP configuration
            username (str): Username for the SNMP configuration
            password (str): Password for the SNMP configuration
            kwargs:
                authentication_algorithm (str): Authentication algorithm for the SNMP configuration
                                                default: HMAC_MD5
                privacy_algorithm (str): Privacy algorithm for the SNMP configuration
                                         default: None
                privacy_password (str): Privacy password for the SNMP configuration
        """
        self._update_config(1, config_hostname, username, password, **kwargs)

    def update(self, config_hostname: str, new_config_hostname: str = None,
               username: str = None, password: str = '', **kwargs) -> None:
        """ Updates an existing SNMP configuration in the Commcell

        Args:
            config_hostname (str): Host name of the SNMP configuration to be updated
            new_config_hostname (str): New host name for the SNMP configuration
            username (str): Username to update SNMP configuration
            password (str): Password to update SNMP configuration
            kwargs:
                authentication_algorithm (str): Authentication algorithm for the SNMP configuration
                                                default: HMAC_MD5
                privacy_algorithm (str): Privacy algorithm for the SNMP configuration
                                         default: None
                privacy_password (str): Privacy password for the SNMP configuration
        """
        if config_hostname not in self.all_configs:
            raise SDKException('Commcell', '102', 'Configuration {0} does not exist'.format(config_hostname))
        old = self.all_configs[config_hostname]
        self._update_config(
            3,
            new_config_hostname or config_hostname,
            username or old['user_name'],
            password,
            id=old['id'],
            authentication_algorithm=kwargs.get("authentication_algorithm", old['authentication_algorithm']),
            privacy_algorithm=kwargs.get("privacy_algorithm", old['privacy_algorithm']),
            privacy_password=kwargs.get("privacy_password", ''),
        )

    def delete(self, config_hostname: str) -> None:
        """ Deletes an SNMP configuration from the Commcell

        Args:
            config_hostname (str): Name of the SNMP configuration to be deleted

        Returns:
            bool: True if the configuration is deleted successfully, False otherwise
        """
        if config_hostname not in self.all_configs:
            raise SDKException('Commcell', '102', 'Configuration {0} does not exist'.format(config_hostname))
        self._update_config(
            2,
            config_hostname,
            self.all_configs[config_hostname]['user_name'],
            authentication_algorithm=self.all_configs[config_hostname]['authentication_algorithm'],
            privacy_algorithm=self.all_configs[config_hostname]['privacy_algorithm'],
        )
