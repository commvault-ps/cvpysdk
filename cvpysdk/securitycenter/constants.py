FQ_PARAMETERS = {"THREAT_DETECTION" :"fq=groups.clientGroup.clientGroupName%3Aneq%3AIndex+Servers&fq=groups.configurationGroupType%3Aeq%3A1"}

UPDATE_TI_PLAN_JSON ={
          "clientGroupOperationType": "Update",
          "clientGroupDetail": {
            "configurationGroupType": 1,
            "tiPlan": {
              "planName": "",
              "planId": 0
            }
          }
        }

RESOURCE_GROUP_PAYLOAD_MANUAL = {
                "name": "",
                "serverGroupType": "MANUAL",
                "manualAssociation": {
                "associatedservers": [

                ]
              }
            }

RESOURCE_GROUP_PAYLOAD_AUTOMATIC = {
    "name": "",
    "serverGroupType": "AUTOMATIC",
    "automaticAssociation": {
        "clientScope": {
            "clientScopeType": "COMMCELL"
        },
        "serverGroupRule": {}
    }
}