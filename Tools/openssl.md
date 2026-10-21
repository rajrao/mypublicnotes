**INSTALLING OPENSSL ON WINDOWS**
1. Open a terminal window in admin mode.
2. Find a suitable OpenSSL install:
```winget search openssl```  
3. Install one. Here I am using (FireDaemon):  
```winget install --id=FireDaemon.OpenSSL -e``
4. Run from insllation folder:
```'C:\Program Files\FireDaemon OpenSSL 4\bin\openssl.exe'```
5. Or add to ENV:
```$Env:PATH += ";C:\Program Files\FireDaemon OpenSSL 4\bin"```

---

**CREATE A NEW RSA KEY PAIR IN PEM FORMAT USING OPENSSL**

1. Create a new key pair:  
```openssl genrsa -out privatekey.pem 2048```  
2. The generated "privatekey.pem" file contains both your private key and your public key. You will need the private key to authenticate access to the service account. Keep this file, and
secure it from unauthorized access. Do not share this file outside your organization.  
3. Extract only the the public key:  
```openssl rsa -in privatekey.pem -pubout -out publickey.pem```
4. The "publickey.pem" file contains the PEM formatted public key needed by PROS Home. This file can be shared with other parties, if necessary.

---  
**EXTRACT THE PUBLIC KEY FROM AN EXISTING X.509 CERTIFICATE USING OPENSSL**

1. Certificates contain the public key and additional data, but do not contain private keys. You will need access to the corresponding private key to authenticate access to the service
account.  
2. Locate or download the X.509 certificate file. This example uses the file name "certificate_filename.crt".  
3. Use OpenSSL to extract the public key:  
```openssl x509 -in certificate_filename.crt -noout -pubkey -out publickey.pem```
4. The "publickey.pem" file contains the PEM formatted public key needed by PROS Portal. This file can be shared with other parties, if necessary.
