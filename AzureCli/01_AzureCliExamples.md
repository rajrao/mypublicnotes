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


# Query Syntax for AZ Commands #

The query syntax that AZ commands take as input is based on [jmespath specifciation](http://jmespath.org/).

# Other useful info #

Pipe command output to file: | out-file xxxxx.txt

