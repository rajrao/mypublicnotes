az configure --defaults group=learn-06cc137b-5b8c-411f-a3fa-fc8e7de65752 sql-server

az is also known as the Azure CLI. It's the command-line interface for working with Azure resources. You'll use this to get information about your database, including the connection string.
jq is a command-line JSON parser. You'll pipe output from az commands to this tool to extract important fields from JSON output.
sqlcmd enables you to execute statements on SQL Server. You'll use sqlcmd to create an interactive session with your Azure SQL database.


|sm|description|command|notes|
|---|---|---|---|
|1|set defaults|az configure --defaults group=learn-06cc137b-5b8c-411f-a3fa-fc8e7de65752 sql-server=[server-name]||
|1|list databases|az sql db list||
|2|use jq|az sql db list \| jq '[.[] \| {name: .name}]'|See below|
|3|use quer|az sql db list --query '[].name'||
|4|show info|az sql db show --name Logistics||
|5|show info using jq|az sql db show --name Logistics \| jq '{name: .name, maxSizeBytes: .maxSizeBytes, status: .status}'||
|6|show conn string|az sql db show-connection-string --client sqlcmd --name Logistics|outputs connstring that can be used to connect to db|
|7|||||
|8|||||
|||||


**Create a postgre sql server**

az postgres server create \
   --name wingtiptoys \
   --resource-group learn-f7a5053f-ed3a-4bfb-ada8-2c80957e6d26 \
   --location centralus \
   --sku-name B_Gen5_1 \
   --storage-size 20480 \
   --backup-retention 15 \
   --version 10 \
   --admin-user "azureuser" \
   --admin-password "P@ssw0rd"
 
**Firewall rule for postgre server**

az postgres server firewall-rule create \
  --resource-group learn-f7a5053f-ed3a-4bfb-ada8-2c80957e6d26 \
  --server <server-name> \
  --name AllowAll \
  --start-ip-address 0.0.0.0 \
  --end-ip-address 255.255.255.255
    
**Remove firewall rule**

az postgres server firewall-rule delete \
  --name AllowAll \
  --resource-group learn-f7a5053f-ed3a-4bfb-ada8-2c80957e6d26 \
  --server-name <server-name>
    
**create sql server**

ADMIN_LOGIN="ServerAdmin"
RESOURCE_GROUP=learn-602f85a5-8191-47f6-b10b-222ee078d8a0
SERVERNAME=FitnessSQLServer-$RANDOM
LOCATION=<location>
PASSWORD=<password>

az sql server create \
--name $SERVERNAME \
--resource-group $RESOURCE_GROUP \
--location $LOCATION \
--admin-user $ADMIN_LOGIN \
--admin-password $PASSWORD

**create sql db**

az sql db create \
--resource-group $RESOURCE_GROUP \
--server $SERVERNAME \
--name FitnessVancouverDB


    


**Outputs:**

**2**
az sql db list | jq '[.[] | {name: .name}]'

    [
      {
        "name": "Logistics"
      },
      {
        "name": "master"
      }
    ]
    
**3**
use quer|az sql db list --query '[].name'
    [
      "Logistics",
      "master"
    ]
    

**Active Directory**

      New-AzRoleAssignment -ObjectId (Get-AzADGroup -SearchString 'Contoso Security Team')[0].Id -RoleDefinitionName "key vault Contributor" -ResourceGroupName ContosoAppRG
      New-AzRoleAssignment -ObjectId (Get-AzADGroup -SearchString 'Contoso Security Team')[0].Id -RoleDefinitionName "User Access Administrator" -ResourceGroupName ContosoAppRG
      
(Secure KeyVault)[https://docs.microsoft.com/en-us/azure/key-vault/general/secure-your-key-vault]
