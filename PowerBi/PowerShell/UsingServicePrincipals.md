Follow the steps outlined: https://docs.microsoft.com/en-us/power-bi/developer/embedded/embed-service-principal

To test using PowerShell

```
function ConnectToPbi
{
    $applicationId = "APPID-GUID";
    $securePassword = "SECRET" | ConvertTo-SecureString -AsPlainText -Force
    $credential = New-Object -TypeName System.Management.Automation.PSCredential -ArgumentList $applicationId, $securePassword
    Connect-PowerBIServiceAccount -ServicePrincipal -Credential $credential -TenantId "TenantId-GUID"
}
```
