"""
A simple script that demonstrates calling PowerBI rest api using MSAL

Sample env.config used in line 27
{
    "authorityUrl": "https://login.microsoftonline.com/{organization-ad-id}",
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
# pip install msal
import msal

# Enable DEBUG log for entire script
# logging.basicConfig(level=logging.DEBUG)
# Optionally disable MSAL DEBUG logs
# logging.getLogger("msal").setLevel(logging.INFO)

config = json.load(open('env.config', encoding="utf-8"))

app = msal.ConfidentialClientApplication(
    config["client_id"], authority=config["authorityUrl"],
    client_credential=config["secret"]
)

result = app.acquire_token_silent(config["scope"], account=None)

if not result:
    logging.info("No suitable token exists in cache. \
                 Let's get a new one from AAD.")
    result = app.acquire_token_for_client(scopes=config["scope"])

groupId = config["group_id"]
datasetId = config["dataset_id"]
if "access_token" in result:
    print("access_token retrieved!")

    token = result['access_token']
    response = requests.get(
        f"https://api.powerbi.com/v1.0/myorg/groups/{groupId}/datasets/\
{datasetId}/refreshes",
        headers={'Authorization': f"Bearer {token}"})
    response.raise_for_status()
    jsonData = response.json()
    print(f"API call result: {json.dumps(jsonData, indent=2)}")

else:
    print(result.get("error"))
    print(result.get("error_description"))
    # You may need this when reporting a bug
    print(result.get("correlation_id"))
