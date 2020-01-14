# Useful Links #
[Azure Command-Line Interface (CLI)](https://docs.microsoft.com/en-us/cli/azure/?view=azure-cli-latest)</br>
[Query Azure CLI command output](https://docs.microsoft.com/en-us/cli/azure/query-azure-cli?view=azure-cli-latest)</br>
[Output Formats](https://docs.microsoft.com/en-us/cli/azure/format-output-azure-cli?view=azure-cli-latest)</br>
[Github Repo](https://github.com/Azure/azure-cli)</br>

# Commands #

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
|*Service Prinicples*||||
||List service principles 1|az ad sp list --all --output table --query "[?contains(objectId, 'xxxxxxxx-xxxx-')]"| find sp with a certain Id|
||List service principles 2|az ad sp list --all --query "[?contains(displayName, 'spNameToSearch')][].{o:objectId name:displayName}" -o json|find sp with a certain name and display the name|
|*Groups*||||
||Find Group|az ad group list --query "[?contains(displayName,'[GroupName]')].{DisplayName:displayName, Id:objectId}" --output table ||
||List group memebers|az ad group member list --group [groupName] --query "[].{displayName:displayName}" --out table||
||Add owner to group|az ad group owner add --group groupId --owner-object-id ownerId||
||Add member to group|az ad group member add --group xxxxxx-yyyyy-guid --member-id xxxxx-yyyy-guid||
|*Users*||||
||Find user|az ad user list --upn "x@y.com" --query [].objectId||
|**Service Bus**||||
||List Topics|az servicebus topic list --namespace-name [namespace name] --resource-group [rg name]||
||create topic|az servicebus topic create --resource-group [rg name] --namespace-name [namespace name] --name [topic name] --enable-ordering true --default-message-time-to-live P30D||
||List topics with name|az servicebus topic list --namespace-name [namespace name] --resource-group [rg name] --query "[?name=='xxxxx'].[name]" --output table|list topic with name xxxxx|
||List topics containing name|az servicebus topic list --namespace-name [namespace name] --resource-group [rg name] --query "[?contains(name,'yyy-')].[name]" --output table|find topics where name contains yyy-|
||List topics begining with name|az servicebus topic list --namespace-name [namespace name] --resource-group [rg name] --query "[?starts_with(name,'qa-')].[name]" --output table|starts with qa-|
||List topics begining with name in sorted order|az servicebus topic list --namespace-name -namespace-name [namespace name] --resource-group [rg name] --query "sort_by([?starts_with(name,'qa-')].{n:name},&n)" --output table||
|**Sql Server**||||
||List Admins|az sql server ad-admin list --server-name [servername] --resource-group [RGNAME] -o table||
|**Cloud Drive**||||
||df|list cloud drive mount info||
||clouddrive|commands to manage cloudDrive||
|||||
|**KeyVault**||||
||List Keyvaults and a property|az keyvault list --query "[].name" -o tsv \| foreach {az keyvault show --name $_ --query "{name:name,enableSoftDelete:properties.enableSoftDelete}"}||
|||||



# Query Syntax for AZ Commands #

The query syntax that AZ commands take as input is based on [jmespath specifciation](http://jmespath.org/).

