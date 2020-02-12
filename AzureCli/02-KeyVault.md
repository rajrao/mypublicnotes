**1. List secrets**

        az keyvault secret list --vault keyVaultName
        
**1. List secrets where name contains QA and sort it **

        az keyvault secret list --vault keyVaultName --query "sort_by([?contains(id,'qa-')].{id:id},&id)" --output tsv
        
**1.         
        
        az keyvault secret list --vault uxKeyVaultDev --query "sort_by([?contains(id,'qa-')].{id:id},&id)" --output tsv | foreach { az keyvault secret show --id "$_" --vault uxKeyVaultDev --query "[].{id:id, value:value}" }
