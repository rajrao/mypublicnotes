Important folder locations

|Type | Location | Notes
|-----|----------|------|
|Installation Folder | C:\Program Files\On-premises data gateway|
|Default Log Location| C:\Windows\ServiceProfiles\PBIEgwService\AppData\Local\Microsoft\On-premises data gateway|Used when you are running using the default local service account: PBIEgwService
|Custom Service Account Log Location|C:\Users\{ServiceAccount}\AppData\Local\Microsoft\On-premises data gateway|Used when running as a custom service account


**SSO Setup**
1. You will need RSAT tools for administration.
2. Helpful documentation: https://docs.microsoft.com/en-us/power-bi/connect-data/service-gateway-sso-kerberos
3. 


**Remote Server Administration Tools** 

1. Server Manager:
    1. Open Server Manager
    2. Add roles and features
    3. Click on "Role-based or feature-based installation"
    4. Go to features.
    5. Under Remote Server Administration Tools, Role Administration Tools, pick "AD DS and AD LDS Tools"

2. Ways to install: https://answers.microsoft.com/en-us/windows/forum/all/rsat-and-all-other-optional-features-missing-in/f709ec1c-18a8-46b7-9d7c-a863e32a33b2?auth=1
3. Download: https://www.microsoft.com/en-us/download/confirmation.aspx?id=45520

