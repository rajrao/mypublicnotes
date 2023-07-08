#a basic demo of how to interact with a rest-api using python and oauth
#implements getting a token and checking for expiration
#uses zoom api as an example

import sys
import requests
import json
import logging
import io
import base64
from datetime import datetime, timedelta, timezone

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)


class ZoomApi:
    def __init__(self, client_id, client_secret, account_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://api.zoom.us/v2/'
        self.auth_url = 'https://zoom.us/oauth/token'
        self.account_id = account_id
        self.access_headers = None
        self.access_token_expires_at = None

    def __get_access_token(self):
        if (self.access_token_expires_at is not None
            and datetime.now(timezone.utc) < self.access_token_expires_at):
            return

        self.access_headers = None
        self.access_token_expires_at = None

        access_token = None
        access_token_response = requests.post(self.auth_url,
                                              auth=(self.client_id,
                                                    self.client_secret),
                                              data={"grant_type": "account_credentials",
                                                    "account_id": f"{account_id}"}, verify=True)
        if access_token_response.ok:
            json = access_token_response.json()
            access_token = json.get('access_token')
            expires_in = int(json.get("expires_in"))
            self.access_token_expires_at = datetime.now(timezone.utc) + timedelta(seconds=expires_in-60)
            _logger.debug(access_token_response.text)
            self.access_headers = {
                'Authorization': 'Bearer ' + access_token,
                "Content-Type": "application/json"
                }
        else:
            self.access_headers = None
            self.access_token_expires_at = None
            _logger.info('Access Token Issue: %s', access_token_response.text)
            raise Exception(f"Access token was not retrieved {access_token_response.text}")
    
    def get_data(self, url) -> dict:
        self.__get_access_token()
        _logger.debug("Url: %s", url)
        response = requests.get(url, headers=self.access_headers)
        if (response.status_code == 401):
            # access_token may have experied so lets get attempt to get token
            _logger.debug("received 401!!")
            _logger.info("Response: %s", response.text)
            #
            _logger.debug("attempting to get a new token....")
            self.__get_access_token()
            _logger.debug("trying with a new token....")
            response = requests.get(url, headers=self.access_headers)

        response.raise_for_status()

        data = response.json()
        _logger.debug(response.text[:100])
        return data

    def get_users(self) -> dict:
        url = f"https://api.zoom.us/v2/users?status=active"
        return self.get_data(url)
    
    def get_user_settings(self, user_id) -> dict:
        url = f"https://api.zoom.us/v2/users/{user_id}/settings"
        return self.get_data(url)

    def get_webinar_list(self, user_id) -> dict:
        url = f"https://api.zoom.us/v2/users/{user_id}/webinars"
        return self.get_data(url)

    def get_webinar_details(self, webinar_id) -> dict:
        url = f"https://api.zoom.us/v2/report/webinars/{webinar_id}"
        return self.get_data(url)
    
    def query_graphql(self, query) -> dict:
        url = f"https://api.zoom.us/v3/graphql"
        self.__get_access_token()
        _logger.debug("Url: %s", url)
        response = requests.post(url, json={'query': query}, headers=self.access_headers)
        if (response.status_code == 401):
            # access_token may have experied so lets get attempt to get token
            _logger.debug("received 401!!")
            _logger.info("Response: %s", response.text)
            #
            _logger.debug("attempting to get a new token....")
            self.__get_access_token()
            _logger.debug("trying with a new token....")
            response = requests.get(url, headers=self.access_headers)

        response.raise_for_status()

        data = response.json()
        _logger.debug(response.text[:100])
        return data

logging.basicConfig(level="INFO")
client_id = ""
client_secret = ""
account_id = ''

_zoomApi = ZoomApi(client_id, client_secret, account_id)
users_response = _zoomApi.get_users()
for user in users_response["users"]:
    user_id = user["employee_unique_id"]
    user_settings = _zoomApi.get_user_settings(user_id)
    if (user_settings["feature"]["webinar"]):
        webinars = _zoomApi.get_webinar_list(user_id)
