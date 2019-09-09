**List Keys**
```
az servicebus namespace authorization-rule keys  list --resource-group rgName --namespace-name nsName --name policyName
```

**update key** autogenerate keyvalue
```
az servicebus namespace authorization-rule keys  renew --resource-group rgName --namespace-name nsName --name policyName --key primaryKey
```
**update key** update to user provided value
```
az servicebus namespace authorization-rule keys  renew --resource-group rgName --namespace-name nsName --name policyName --key primaryKey --key-value "xxxxxxxxxxxxxxxxxxxxxx="
```
