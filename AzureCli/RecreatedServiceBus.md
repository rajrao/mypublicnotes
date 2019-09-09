# Recreating ServiceBus #

1. **Export entities** using ServiceBusExplorer from the existing ASB namespace.
1. **Create a new ServiceBus** (or delete the old one). *Note: if you need Zone Redunancy with Premium sku, you currently need to do it via the Portal or a different mechanism as AZ CLI doesnt support it yet.*
   > az servicebus namespace create --resource-group testinstancefordev --name testfordelete1 --capacity 1 --location "West US" --sku Premium
1. **Update primary key**
   > az servicebus namespace authorization-rule keys  renew --resource-group testinstancefordev --namespace-name testfordelete1 --name RootManageSharedAccessKey --key primaryKey --key-value "vn041Y5PYexZRUoqXjI4GmXMsPFGcG5nBPP80uEEtEo="
1. **Update secondary key**
   > az servicebus namespace authorization-rule keys  renew --resource-group testinstancefordev --namespace-name testfordelete1 --name RootManageSharedAccessKey --key secondaryKey --key-value "SFHK8W5V3odWo/cgyle9EJAqKmVF3dXDneFjWH1/eoc="
1. **Import entities** into new Service Bus namespace using ServiceBus Explorer.
1. **Delete if testing**
   > az servicebus namespace delete --resource-group testinstancefordev --name testfordelete1
