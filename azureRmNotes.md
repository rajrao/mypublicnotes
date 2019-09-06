Azure Notes


1. Install AzureRM PS: https://docs.microsoft.com/en-us/powershell/azure/install-azurerm-ps
2. ARM templates: https://docs.microsoft.com/en-us/azure/azure-resource-manager/resource-manager-export-template-powershell
3. New-AzureRmServiceBusTopic -ResourceGroupName testinstanceRg -Namespace testinstance -TopicName HelloWorld1 -DefaultMessageTimeToLive 1001 -EnablePartitioning $true
4. In devOps, as a step: New-AzureRmServiceBusTopic -ResourceGroupName $env:ServiceBusResourceGroup -Namespace $env:ServiceBusNamespace -TopicName $env:AzureTopicName -EnablePartitioning $False
5. Get-AzureRmResourceGroup
6. Get-AzureRmResource
7. Get-AzureRmResource -ResourceType Microsoft.ServiceBus/namespaces
8. Get-AzureRmADApplication -DisplayNameStartWith MyDemoWebApp
9. Set-AzureRmAppServicePlan -ResourceGroupName [rg name] -Name [name] -Tier Free
10. 




Get-AzureRmResourceProvider -ListAvailable | Select-Object ProviderNamespace, RegistrationState
get-AzureRmResourceProvider -ListAvailable |where {$_.Registrationstate -eq "Registered"}
Register-AzureRmResourceProvider -ProviderNamespace Microsoft.Devices
	Microsoft.Storage
	Microsoft.DataBricks
	Microsoft.MachineLearning

get-AzureRmResourceProvider -ListAvailable | select ProviderNamespace
get-AzureRmResourceProvider -ListAvailable |where {$_.ProviderNamespace.StartsWith("Microsoft.")}
Register all available providers: (Warning can take a long time!)
get-AzureRmResourceProvider -ListAvailable |where {$_.ProviderNamespace.StartsWith("Microsoft.") -and $_.Registrationstate -eq "NotRegistered"} | foreach-object{Register-AzureRmResourceProvider -ProviderNamespace $_.ProviderNamespace}

Get-AzureRmResourceProvider -ListAvailable | Where-Object { $_.RegistrationState -eq 'NotRegistered'} | Register-AzureRmResourceProvider
	From <https://stackoverflow.com/questions/43987219/in-azure-how-to-allow-non-subscription-admins-to-create-new-resources> 


Add MSI to a group
connect-azuread -tenantid [tenant GUID]
Create the group
	$Group = New-AzureADGroup -DisplayName "AdGroupName" -MailEnabled $false -SecurityEnabled $true -MailNickName "NotSet"
Add the SP to the group. (Use Service IdentityId and not the Service Identity Application Id)
	Add-AzureAdGroupMember -ObjectId $Group.ObjectId -RefObjectId "[IdentityId]"
Setup permissions on the group
