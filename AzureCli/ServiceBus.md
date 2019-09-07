**List Keys**
az servicebus namespace authorization-rule keys  list --resource-group rgName --namespace-name nsName --name policyName

**update key** autogenerate keyvalue
az servicebus namespace authorization-rule keys  renew --resource-group rgName --namespace-name nsName --name policyName --key primaryKey

**update key** update to user provided value
az servicebus namespace authorization-rule keys  renew --resource-group rgName --namespace-name nsName --name policyName --key primaryKey --key-value "xxxxxxxxxxxxxxxxxxxxxx="





Recreating ServiceBus

1. Export entities using ServiceBusExplorer.
2. Create a new ServiceBus (or delete the old one). Note if you need Zone Redunancy with Premium sku, you currently need to do it via the Portal or a different mechanism as AZ CLI doesnt support it yet.
az servicebus namespace create --resource-group testinstanceforncmdev --name testfordelete1 --capacity 1 --location "West US" --sku Premium
3. Update primary key 
az servicebus namespace authorization-rule keys  renew --resource-group testinstanceforncmdev --namespace-name testfordelete1 --name RootManageSharedAccessKey --key primaryKey --key-value "vn041Y5PYexZRUoqXjI4GmXMsPFGcG5nBPP80uEEtEo="
4. Update secondary key
az servicebus namespace authorization-rule keys  renew --resource-group testinstanceforncmdev --namespace-name testfordelete1 --name RootManageSharedAccessKey --key secondaryKey --key-value "SFHK8W5V3odWo/cgyle9EJAqKmVF3dXDneFjWH1/eoc="
5. Import entities into new Service Bus namespace using ServiceBus Explorer.
6. **Delete if testing**
az servicebus namespace delete --resource-group testinstanceforncmdev --name testfordelete1
