1. Setting up app-settings to pull data from Azure KeyVault:
Format the appsetting value as follows: @Microsoft.KeyVault(SecretUri=https://vaultname.vault.azure.net/secrets/secretname-versionGuid/)
  eg: @Microsoft.KeyVault(SecretUri=https://myvault.vault.azure.net/secrets/helloworld-8ff7e5af-c042-457e-8186-caca99a814af/)
