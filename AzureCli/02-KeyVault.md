1. **List secrets**

    az keyvault secret list --vault keyVaultName
    
    az keyvault secret list --vault [Name] --output table
  
  spits out only the id
    
    az keyvault secret list --vault [Name] --query "[].{objectId:id}" --out table

2. **List secrets where name contains QA and sort it**

    az keyvault secret list --vault keyVaultName --query "sort_by([?contains(id,'qa-')].{id:id},&id)" --output tsv
    
    az keyvault secret list --vault [Name] --query "sort_by([].{objectId:id}, &objectId)" --out table

3. **List keyvalults with keyvault property

    az keyvault list --query "[].name" -o tsv | foreach {az keyvault show --name $_ --query "{name:name,enableSoftDelete:properties.enableSoftDelete}"}
    
4. **List keyvault secrets that start with qa or uat and output updated property **
   
    az keyvault secret list --vault-name kyName --query "sort_by([?contains(id,'qa-') || contains(id,'uat-') ].{id:id,updated:attributes.updated},&id)" -o tsv
   
5. **List secrets where name contains QA and also output the secret and date created and updated.**      
        
       az keyvault secret list --vault keyVaultName --query "sort_by([?contains(id,'qa-')].{id:id},&id)" --output tsv | foreach { az keyvault secret show --id "$_" --vault keyVaultName --output json --query "{name:id, value:value, created:attributes.created, updated:attributes.updated}" --output tsv }

or

    $keyContains = "qa-"
    $keyVaultName="keyVaultName"
    
    $secrets = az keyvault secret list --vault $keyVaultName --query "sort_by([?contains(id,'$keyContains')].{id:id},&id)" --output tsv
    foreach ($secret in $secrets)
    {
        az keyvault secret show --id "$secret" --vault $keyVaultName --output json --query "{id:id, value:value, created:attributes.created, updated:attributes.updated}" --output tsv
    }
    
6. **List modified dates on secrets **

        az keyvault secret list --vault uxkeyvaultdev --query "sort_by([?contains(id,'qa-') || contains(id,'uat-') ].{id:id,updated:attributes.updated},&id)" -o tsv
