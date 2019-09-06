||**Description**|**Command**|**Notes**|
|---|---|---|---|
|||||
|**Login**||az login|not needed in cloud shell, only when running from local machine|
|Select subscription||az account set --subscription "[subscription name]"|az account set --subscription "Development Subscription"|
|**KeyValult**||||
||List Secrets| az keyvault secret list --vault-name [Name] --output table||
||List Secrets|  az keyvault secret list --vault-name [Name] --query "[].{objectId:id}" --out table|spits out only the id|
||List Secrets|  az keyvault secret list --vault-name [Name] --query "sort_by([].{objectId:id}, &objectId)" --out table||
|**Active Directory**||||
||List service principles 1|az ad sp list --all --output table --query "[?contains(objectId, 'xxxxxxxx-xxxx-')]"| find sp with a certain Id|
||List service principles 2|az ad sp list --all --query "[?contains(displayName, 'spNameToSearch')][].{o:objectId name:displayName}" -o json|find sp with a certain name and display the name|
||List group memebers|az ad group member list --group [groupName] --query "[].{displayName:displayName}" --out table||
|**Service Bus**||||
||List Topics|az servicebus topic list --namespace-name [namespace name] --resource-group [rg name]||
||create topic|az servicebus topic create --resource-group [rg name] --namespace-name [namespace name] --name [topic name]||
|||||
|||||
|||||

