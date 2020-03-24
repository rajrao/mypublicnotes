||**Description**|**Command**|**Notes**|
|---|---|---|---|
|||||
|**Active Directory**||||
|*Service Prinicples*||||
||List service principles 1|az ad sp list --all --output table --query "[?contains(objectId, 'xxxxxxxx-xxxx-')]"| find sp with a certain Id|
||Get Service Principal using objectId|$sp = Get-AzureADServicePrincipal -ObjectId "xxxxx-xxxx-xxxxx"||
||Get Assignments|$assignments = Get-AzureADServiceAppRoleAssignment -ObjectId $sp.ObjectId -All $true <br> $assignments \| ForEach-Object { ....}||
|||||
||List service principles 2|az ad sp list --all --query "[?contains(displayName, 'spNameToSearch')][].{o:objectId name:displayName}" -o json|find sp with a certain name and display the name|
||List service principles with return urls|az ad sp list --query "[].{dn:appDisplayName,appId:appId,o:objectId,r:replyUrls}"||
|*Groups*||||
||Find Group|az ad group list --query "[?contains(displayName,'[GroupName]')].{DisplayName:displayName, Id:objectId}" --output table ||
||List group memebers|az ad group member list --group [groupName] --query "[].{displayName:displayName}" --out table||
||Add owner to group|az ad group owner add --group groupId --owner-object-id ownerId||
||Add member to group|az ad group member add --group xxxxxx-yyyyy-guid --member-id xxxxx-yyyy-guid||
|*Users*||||
||Find user|az ad user list --upn "x@y.com" --query [].objectId||
