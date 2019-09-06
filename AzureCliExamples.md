||**Description**|**Command**|**Notes**|
|---|---|---|---|
|||||
|**Login**||az login|not needed in cloud shell, only when running from local machine|
|Select subscription||az account set --subscription "[subscription name]"|az account set --subscription "Development Subscription"|
|**KeyValult**||||
||List Secrets| az keyvault secret list --vault-name [Name] --output table||
||List Secrets|  az keyvault secret list --vault-name [Name] --query "[].{objectId:id}" --out table|spits out only the id|
||List Secrets|  az keyvault secret list --vault-name [Name] --query "sort_by([].{objectId:id}, &objectId)" --out table|sorts by name and spits out the id|
|**Active Directory**||||
||List service principles 1|az ad sp list --all --output table --query "[?contains(objectId, 'xxxxxxxx-xxxx-')]"| find sp with a certain Id|
||List service principles 2|az ad sp list --all --query "[?contains(displayName, 'spNameToSearch')][].{o:objectId name:displayName}" -o json|find sp with a certain name and display the name|
||List group memebers|az ad group member list --group [groupName] --query "[].{displayName:displayName}" --out table||
||Find Group|az ad group list --query "[?contains(displayName,'[GroupName]')].{DisplayName:displayName, Id:objectId}" --output ||
||Add owner to group|az ad group owner add --group groupId --owner-object-id ownerId||
||Add member to group|az ad group member add --group xxxxxx-yyyyy-guid --member-id xxxxx-yyyy-guid||
||Find user|az ad user list --upn "x@y.com" --query [].objectId||
|**Service Bus**||||
||List Topics|az servicebus topic list --namespace-name [namespace name] --resource-group [rg name]||
||create topic|az servicebus topic create --resource-group [rg name] --namespace-name [namespace name] --name [topic name]||
|**Sql Server**||||
||List Admins|az sql server ad-admin list --server-name [servername] --resource-group [RGNAME] -o table||
|||||

