**Active Directory**

||**Description**|**Command**|**Notes**|
|---|---|---|---|
|||||
|*Service Prinicples*||||
||List service principles 1|az ad sp list --all --output table --query "[?contains(objectId, 'xxxxxxxx-xxxx-')]"| find sp with a certain Id|
||Find service principles query by appId|az ad sp list --all --output table --query "[?contains(appId, 'xxxxxxxx-xxxx-')]"||
||List service principles 2|az ad sp list --all --query "[?contains(displayName, 'spNameToSearch')][].{o:objectId name:displayName}" -o json|find sp with a certain name and display the name|
||List service principles with return urls|az ad sp list --query "[].{dn:appDisplayName,appId:appId,o:objectId,r:replyUrls}"||
||Output to text file all SPNs|az ad sp list --all --query "[].{dn:appDisplayName,appId:appId,o:objectId,r:replyUrls}" \| out-file splist.txt||
||Get Service Principal using objectId|$sp = Get-AzureADServicePrincipal -ObjectId "xxxxx-xxxx-xxxxx"||
||Get Assignments|$assignments = Get-AzureADServiceAppRoleAssignment -ObjectId $sp.ObjectId -All $true <br> $assignments \| ForEach-Object { ....}||
|||||


||**Description**|**Command**|**Notes**|
|---|---|---|---|
|||||
|*Groups*||||
||Find Group|az ad group list --query "[?contains(displayName,'[GroupName]')].{DisplayName:displayName, Id:objectId}" --output table ||
||List group memebers|az ad group member list --group [groupName] --query "[].{displayName:displayName}" --out table||
||Search for a member in a group|az ad group member list --group GROUP_NAME --query "[].{dn:displayName} | [?starts_with(dn,'Joe')]"||
||Add owner to group|az ad group owner add --group groupId --owner-object-id ownerId||
||Add member to group|az ad group member add --group xxxxxx-yyyyy-guid --member-id xxxxx-yyyy-guid||
|||||




||**Description**|**Command**|**Notes**|
|---|---|---|---|
|||||
|*Users*||||
||Find user|az ad user list --upn "x@y.com" --query [].objectId||
|||||

Remove all users assigned to the application

    Connect-AzureAD
    # Get Service Principal using objectId
    $sp = Get-AzureADServicePrincipal -ObjectId "82c0f9e1-ee00-4de4-8578-d8d2abac51ec"

    # Get Azure AD App role assignments using objectId of the Service Principal
    $assignments = Get-AzureADServiceAppRoleAssignment -ObjectId $sp.ObjectId -All $true

    # Remove all users and groups assigned to the application
    $assignments | ForEach-Object {
        if ($_.PrincipalType -eq "User") {
            Remove-AzureADUserAppRoleAssignment -ObjectId $_.PrincipalId -AppRoleAssignmentId $_.ObjectId
        } elseif ($_.PrincipalType -eq "Group") {
            Remove-AzureADGroupAppRoleAssignment -ObjectId $_.PrincipalId -AppRoleAssignmentId $_.ObjectId
        }
    }
    
Revoke all permissions granted to the application

    Connect-AzureAD

    # Get Service Principal using objectId
    $sp = Get-AzureADServicePrincipal -ObjectId "82c0f9e1-ee00-4de4-8578-d8d2abac51ec"

    # Get all delegated permissions for the service principal
    $spOAuth2PermissionsGrants = Get-AzureADOAuth2PermissionGrant -All $true| Where-Object { $_.clientId -eq $sp.ObjectId }

    # Remove all delegated permissions
    $spOAuth2PermissionsGrants | ForEach-Object {
        Remove-AzureADOAuth2PermissionGrant -ObjectId $_.ObjectId
    }

    # Get all application permissions for the service principal
    $spApplicationPermissions = Get-AzureADServiceAppRoleAssignedTo -ObjectId $sp.ObjectId -All $true | Where-Object { $_.PrincipalType -eq "ServicePrincipal" }

    # Remove all delegated permissions
    $spApplicationPermissions | ForEach-Object {
        Remove-AzureADServiceAppRoleAssignment -ObjectId $_.PrincipalId -AppRoleAssignmentId $_.objectId
    }
    
Revoke refresh tokens for all users
    
    Connect-AzureAD

    # Get Service Principal using objectId
    $sp = Get-AzureADServicePrincipal -ObjectId "82c0f9e1-ee00-4de4-8578-d8d2abac51ec"

    # Get Azure AD App role assignments using objectID of the Service Principal
    $assignments = Get-AzureADServiceAppRoleAssignment -ObjectId $sp.ObjectId -All $true | Where-Object {$_.PrincipalType -eq "User"}

    # Revoke refresh token for all users assigned to the application
    $assignments | ForEach-Object {
        Revoke-AzureADUserAllRefreshToken -ObjectId $_.PrincipalId
    }
