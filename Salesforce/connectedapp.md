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
