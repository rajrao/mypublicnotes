import sys
import requests
import json
import logging
import io

_logger = logging.getLogger(__name__)
_logger.setLevel(logging.DEBUG)

class RestApiSampleAPI:
    def __init__(self, client_id, client_secret, account_id):
        self.client_id = client_id
        self.client_secret = client_secret
        self.base_url = 'https://xyc.com'
        self.auth_url = 'https://oauth.xyc.com/access_token'
        self.access_headers = None

    def __get_access_token(self):
        access_token = None
        access_token_response = requests.post(self.auth_url
                                            ,params="grant_type=client_credentials"
                                            ,auth=(self.client_id, self.client_secret)
                                            ,verify=True)
        if access_token_response.ok:
            access_token = access_token_response.json().get('access_token')
            _logger.debug(access_token_response.text)
            self.access_headers = { 'Authorization': 'Bearer ' + access_token, "Content-Type": "application/json" }
        else:
            self.access_headers = None
            _logger.info('Access Token Issue: %s', access_token_response.text)
            raise Exception(f"Access token was not retrieved {access_token_response.text}")
        
        
    
    def get_data(self) -> str:
        
        self.__get_access_token()
        data_url = f'{self.base_url}/data/'\
          'abcd?field1=a&field2=b'

        _logger.debug("Url: %s", data_url)
        response = requests.get(data_url,headers=self.access_headers)
        
        if(response.status_code == 401):
            #access_token may have experied so lets get attempt to get token
            _logger.debug("received 401!!")
            _logger.info("Response: %s",response.text)
            
            _logger.debug("attempting to get a new token....")
            self.__get_access_token()
            
            _logger.debug("trying with a new token....")
            response = requests.get(data_url, headers=self.access_headers)

        response.raise_for_status()

        data = response.json()
        return data

logging.basicConfig(level="INFO")
client_id = ""
client_secret = ""

api = RestApiSampleAPI(client_id, client_secret, account_id)
data = api.get_data()

#test1
with open("data.json", "w") as file:
    file.write(data)


