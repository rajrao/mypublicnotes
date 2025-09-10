You will need a private and public key

1. openssl genrsa -out keypair.pem 2048
2. openssl req -new -x509 -nodes -sha256 -days 365 -key keypair.pem -out certificate.crt
3. openssl pkcs8 -topk8 -nocrypt -in keypair.pem -out private.key


**Sales Force**
* Create Connected App
  * App Manager >> Manage Connected Apps
  * Basic Connected App
  * Provide a user name. Username should be different in each org
  * JWT OAuth Flow
    * Use Digital Signatures
    * Provide the callback url as: https://{org}.sandbox.lightning.force.com/services/oauth/success
    * Add the digital certificate CRT file
    * Set OAuth scopes: API, refresh_Token, offline_access, cdp_ingest_api (for data cloud ingestion), etc
    * Disable:
      * Require Proof of key for code exchange
      * Require secret for web server flow
      * Require secret for refresh token flow
  * When you save, capture the "Consumer Key" this will be used as the client-id
  * Click Save
  * Update Policies:
    * Relax IP Restrictions
    * Refresh token is valid until revoked
    * All users may self-authorize
    * Timeout value: none
* OAuth settings:
  * Allow OAuth username-password flows.
  * Approve the app by clicking through this URL and selecting Allow.
```
https://{org}.sandbox.lightning.force.com/services/oauth2/authorize?response_type=code&client_id={consumer-key}&scope=api refresh_token cdp_ingest_api&redirect_uri=https://{org}.sandbox.lightning.force.com/services/oauth/success&code_challenge=SHA256
```



**Connected App Test Code**
*this code is not for production, its meant to test the connected app setup only. it also shows you how to create the JWT token and cache its value*
```python
import json
import base64
import jwt
import requests
import logging
import time
from datetime import datetime, timedelta
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()

settings ={}
cache = {}
env = None

def _get_token_and_instance_url():
    current_epoch = int(time.time())
    if cache.get('cdp_access_token') and current_epoch < cache.get('cdp_access_token').get('ttl'):
        # Cache Hit
        ttl = cache.get('cdp_access_token').get('ttl')
        print("Cache hit! - token expiring in " + str(ttl - int(time.time())) + " seconds")
        return cache.get('cdp_access_token').get('token'), cache.get('cdp_access_token').get('instance_url')
    else:
        # Cache Miss
        jwt_token, expiry = _get_jwt()
        print('Cache miss! - JWT token generated successfully')
        instance_url = _get_login_url() + '/services/oauth2/token'
        data = {'grant_type': 'urn:ietf:params:oauth:grant-type:jwt-bearer', 'assertion': jwt_token}
        core_response = requests.post(instance_url, data=data)
        core_response.raise_for_status()
        print('Response core access token generated successfully')

        core_access_token = core_response.json()['access_token']
        core_instance_url = core_response.json()['instance_url']
        cdp_data = {'grant_type': 'urn:salesforce:grant-type:external:cdp',
                    'subject_token_type': 'urn:ietf:params:oauth:token-type:access_token',
                    'subject_token': core_access_token}
        cdp_token_path = '/services/a360/token'
        cdp_url = core_instance_url + cdp_token_path
        cdp_response = requests.post(cdp_url, data=cdp_data)
        cdp_response.raise_for_status()
        print('Response cdp access token generated successfully')
        cdp_access_token = cdp_response.json()['access_token']
        instance_url = cdp_response.json()['instance_url']
        cache['cdp_access_token'] = {'token': cdp_access_token, 'ttl': expiry, 'instance_url': instance_url}
        return cdp_access_token, instance_url

def _get_jwt():
    key = _get_rsa_key()
    key = key.strip().splitlines()
    # remove -----BEGIN PRIVATE KEY----- and -----END PRIVATE KEY-----
    stripped_key = (''.join(i for i in key[1:-1] if len(i.strip()) > 0)).strip()
    secret = base64.b64decode(stripped_key)
    due_date = datetime.now() + timedelta(minutes=50)
    iss = _get_consumer_key()
    sub = _get_sf_username()
    aud = _get_audience_url() #_get_login_url()
    expiry = int(due_date.timestamp())
    payload = {"iss": iss, "sub": sub, "exp": expiry, "aud": aud}
    print(json.dumps(payload))
    priv_rsakey = serialization.load_der_private_key(secret, password=None, backend=default_backend())
    token = jwt.encode(payload, priv_rsakey, algorithm='RS256')
    return token, expiry


def _get_sf_username():
    return settings[env]["sf_username"]

def _get_audience_url():
    return settings[env]["sf_audience_url"]

def _get_login_url():
    return settings[env]["sf_login_url"]

def _get_rsa_key():
    return settings[env]["rsa_private_key"]


def _get_consumer_key():
    return settings[env]["sf_consumer_key"]

def _init_settings():
    settings["dev"] ={
            "sf_consumer_key" : "",
            "sf_username" : "",
            "sf_login_url": "https://xxxx.sandbox.my.salesforce.com",
            "sf_audience_url" : "https://test.salesforce.com",
            "rsa_private_key": """
    -----BEGIN PRIVATE KEY-----
    -----END PRIVATE KEY-----
    """
        }
    settings["uat"] = {
            "sf_consumer_key": "",
            "sf_username" :"",
            "sf_login_url" : "https://xxxx.sandbox.my.salesforce.com",
            "sf_audience_url": "https://test.salesforce.com",
            "rsa_private_key": """-----BEGIN PRIVATE KEY-----
    -----END PRIVATE KEY-----"""
        }


env = "dev"
_init_settings()
try:
    cdp_access_token, instance_url = _get_token_and_instance_url()
    logger.info("cdp_access_token: %s",cdp_access_token)
    logger.info("instance_url: %s", instance_url)
except requests.HTTPError as e:
    print(e)
    print(e.response.text)
```
