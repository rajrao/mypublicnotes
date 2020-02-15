**1. List secrets**

        az keyvault secret list --vault keyVaultName
        
**2. List secrets where name contains QA and sort it **

        az keyvault secret list --vault keyVaultName --query "sort_by([?contains(id,'qa-')].{id:id},&id)" --output tsv
        
**3. List sectres where name contains QA and also output the secret and date created and updated.        
        
        az keyvault secret list --vault keyVaultName --query "sort_by([?contains(id,'qa-')].{id:id},&id)" --output tsv | foreach { az keyvault secret show --id "$_" --vault keyVaultName --output json --query "{name:id, value:value, created:attributes.created, updated:attributes.updated}" --output tsv }
