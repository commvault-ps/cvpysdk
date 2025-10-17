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

"""Constants and Enums for Cloud Discovery module."""

from enum import Enum, IntEnum


class AssetProvider(IntEnum):
    """Enumeration for different asset providers."""
    
    NONE = 0
    AZURE = 1
    AWS = 2
    GCP = 3
    M365 = 4
    LOCAL = 5
    COMMVAULT = 6


class WorkloadType(IntEnum):
    """Enumeration for different workload types."""
    
    NONE = 0
    COMPUTE = 1
    STORAGE = 2
    DATABASE = 3
    SECURITY = 4
    APPLICATION = 5


class AssetType(IntEnum):
    """Enumeration for different asset types across cloud providers."""
    
    NONE = 0
    
    # Azure Assets
    AZURE_VIRTUAL_MACHINE = 1
    AZURE_VM_SCALE_SET = 2
    AZURE_KUBERNETES_SERVICE = 3
    AZURE_STORAGE_ACCOUNT = 4
    AZURE_BLOB_STORAGE = 5
    AZURE_FILE_STORAGE = 6
    AZURE_QUEUE_STORAGE = 7
    AZURE_TABLE_STORAGE = 8
    AZURE_COSMOS_DB_ACCOUNT = 9
    AZURE_COSMOS_DB_SQL_ACCOUNT = 10
    AZURE_COSMOS_DB_MONGODB_RU_ACCOUNT = 11
    AZURE_COSMOS_DB_CASSANDRA_RU_ACCOUNT = 12
    AZURE_COSMOS_DB_GREMLIN_ACCOUNT = 13
    AZURE_COSMOS_DB_TABLE_ACCOUNT = 14
    AZURE_SQL_DATABASE = 15
    AZURE_POSTGRESQL_SERVER = 16
    AZURE_MYSQL_SERVER = 17
    AZURE_MYSQL_SERVER_FLEXIBLE = 18
    AZURE_POSTGRESQL_SERVER_FLEXIBLE = 19
    AZURE_DATA_LAKE_STORAGE = 37
    
    # Amazon AWS Assets
    AMAZON_EC2_VIRTUAL_MACHINE = 20
    AMAZON_S3_STORAGE = 21
    AMAZON_RDS = 22
    AMAZON_DYNAMO_DB = 23
    AMAZON_DOCUMENT_DB = 24
    AMAZON_ELASTIC_KUBERNETES_SERVICE = 29
    AMAZON_FSX_FILE_SYSTEM = 30
    
    # Microsoft 365 Assets
    M365_ONEDRIVE_APP = 25
    M365_EXCHANGE_APP = 26
    M365_TEAMS_APP = 27
    M365_SHAREPOINT_APP = 28
    
    # Google Cloud Platform Assets
    GOOGLE_CLOUD_VIRTUAL_MACHINE = 31
    GOOGLE_CLOUD_SQL_DATABASE = 32
    GOOGLE_CLOUD_BIG_QUERY_DATABASE = 33
    GOOGLE_CLOUD_ALLOY_DB_DATABASE = 34
    GOOGLE_CLOUD_FILE_STORAGE = 35
    GOOGLE_CLOUD_CLOUD_SPANNER = 36


class AssetCVProtectionStatus(IntEnum):
    """Enumeration for Commvault protection status of assets."""
    
    NONE = 0
    PROTECTED = 1
    NOT_PROTECTED = 2
    PROTECTION_CONFIGURED = 3