# Sample code showing how to call PowerBi rest api using python.
# Uses a file called "env.config", that provides credential info.
# A very simple script that demonstrates how to use MSAL to call PBI-Rest API
#
# Sample env.config
"""
{
    "authorityUrl": "https://login.microsoftonline.com/{organization-ad-id-here}",
    "client_id": "{client-id-guid-here}",
    "scope": ["https://analysis.windows.net/powerbi/api/.default"],
    "secret": "{client-secret-here}",
    "group_id":"{workspace-guid-here}",
    "dataset_id":"{dataset-guid-here}"
}
"""

import json
import logging

import requests
import msal     #pip install msal

# logging.basicConfig(level=logging.DEBUG)  # Enable DEBUG log for entire script
# logging.getLogger("msal").setLevel(logging.INFO)  # Optionally disable MSAL DEBUG logs

config = json.load(open('env.config'))

app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authorityUrl"],
    client_credential=config["secret"]
)

result = None

result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])

groupId = config["group_id"]
datasetId = config["dataset_id"]
if "access_token" in result:
    print ("access_token retrieved!")

    
    response = requests.get(
        f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/{datasetId}/refreshes",
        headers={'Authorization': 'Bearer ' + result['access_token']})
    response.raise_for_status()
    jsonData = response.json()
    print("API call result: %s" % json.dumps(jsonData, indent=2))

else:
    print(result.get("error"))
    print(result.get("error_description"))
    print(result.get("correlation_id"))  # You may need this when reporting a bug
