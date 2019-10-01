#bash file that creates topics, a subscription called audit and publishes the connection string to keyVault

#to make the file runable
#chmod +x ~/createTopic.sh
#to run it: ~/createTopic.sh

resourceGroupName="MY_SPECIAL_RG"
namespaceName="myServiceBus"
subscription="Development Subscription"
keyVaultName="MyKeyVaultName"
uxAuthorizationRuleName="AuthorizationRuleName"
auditSubscriptionName="audit"
replaceString="xxxxx" #used when updating keyvault

createTopic()
{
	if [ $# -eq 1 ]; then
		topicName=$1
    echo "creating topic $topicName"
		az servicebus topic create --resource-group $resourceGroupName --namespace-name $namespaceName --name $topicName --enable-ordering true --default-message-time-to-live P30D --enable-partitioning false --subscription "$subscription"
		az servicebus topic authorization-rule create --resource-group $resourceGroupName --namespace-name $namespaceName --topic-name $topicName --name $uxAuthorizationRuleName --rights Listen Manage Send --subscription "$subscription"
		az servicebus topic subscription create --name "audit" --resource-group $resourceGroupName --namespace-name $namespaceName --topic-name $topicName --subscription "$subscription"
		#az servicebus topic authorization-rule show --resource-group $resourceGroupName --namespace-name $namespaceName --topic-name $topicName --name $uxAuthorizationRuleName
		keyValue=$(az servicebus topic authorization-rule keys list --resource-group $resourceGroupName --namespace-name $namespaceName --topic-name $topicName --name $uxAuthorizationRuleName --subscription "$subscription" --query "primaryKey")
		connectionStringValue=$(az servicebus topic authorization-rule keys list --resource-group $resourceGroupName --namespace-name $namespaceName --topic-name $topicName --name $uxAuthorizationRuleName --subscription "$subscription" --query "primaryConnectionString")
		##remove quotes around the string
		keyValue=${keyValue//\"/} 
		connectionStringValue=${connectionStringValue//\"/}
		##remove the key from connection string
		connectionStringValue=${connectionStringValue/$keyValue/$replaceString}
		##create secret in keyvault
		az keyvault secret set --vault-name $keyVaultName --name $topicName --value $keyValue --description $connectionStringValue
 
    else
 
        echo "please call createTopic with topic name";
    fi
}

createTopic "MyTopicName"
