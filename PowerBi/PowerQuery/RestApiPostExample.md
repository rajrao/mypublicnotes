Example

from: https://www.bluegranite.com/blog/monitoring-azure-data-factory-v2-using-power-bi

If you get a Web.Content doesnt support authentication, then you will have to go into datasource settings and mark the urls as using anonymous auth.


    let
      //Set variables for authenticating to Azure using Service Principal and making API request
      tenantID = "<tenantid>",
      subscriptionId = "<subid>",
      resourceGroupName = "<rgName>",
      factoryName = "<factoryName>",
      apiVersion = "2018-06-01",
      appId = "<clientId>", //this service principal will need "Data Factory Contributor" role (not sure if there is a more limited role than that available for this
      clientSecrets = "<clientSecret>",
      uri = "https://login.microsoftonline.com/" & tenantID & "/oauth2/token",
      res = "https://management.azure.com/",
      today = DateTime.LocalNow() as datetime,
      prev = Date.AddMonths(today, - 1),
      startDt = DateTime.Date(prev),
      startDtText
        = "'" & Text.From(Date.Year(startDt)) & "-" & Text.From(Date.Month(startDt)) & "-" & Text.From(
          Date.Day(startDt)
        )
          & "T00:00:00.0000000Z'",
      endDt = DateTime.Date(today),
      endDtText
        = "'" & Text.From(Date.Year(endDt)) & "-" & Text.From(Date.Month(endDt)) & "-" & Text.From(
          Date.Day(endDt)
        )
          & "T00:00:00.0000000Z'",
      //Obtain Authorization token for Service Principal
      authBody = [
        grant_type = "client_credentials",
        client_id = appId,
        client_secret = clientSecrets,
        resource = res
      ],
      authQueryString = Uri.BuildQueryString(authBody),
      authHeaders = [#"Accept" = "application/json"],
      auth = Json.Document(
        Web.Contents(uri, [Headers = authHeaders, Content = Text.ToBinary(authQueryString)])
      ),
      token = auth[access_token],
      //Build request URL & Body using variables
      url
        = "https://management.azure.com/subscriptions/" & subscriptionId & "/resourceGroups/"
          & resourceGroupName
          & "/providers/Microsoft.DataFactory/factories/"
          & factoryName
          & "/queryPipelineRuns?api-version="
          & apiVersion,
      reqBody = "{ ""lastUpdatedAfter"": " & startDtText & ", ""lastUpdatedBefore"": " & endDtText
        & " } ] }",
      //Make API Call to query Data Factory
      reqHeaders = [#"Content-Type" = "application/json", #"Authorization" = "Bearer " & token],
      result = Json.Document(
        Web.Contents(url, [Headers = reqHeaders, Content = Text.ToBinary(reqBody)])
      ),
        value = result[value],
        #"Converted to Table" = Table.FromList(value, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
        #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", {"id", "runId", "debugRunId", "runGroupId", "pipelineName", "parameters", "invokedBy", "runStart", "runEnd", "durationInMs", "status", "message", "lastUpdated", "annotations", "runDimension", "isLatest"}, {"id", "runId", "debugRunId", "runGroupId", "pipelineName", "parameters", "invokedBy", "runStart", "runEnd", "durationInMs", "status", "message", "lastUpdated", "annotations", "runDimension", "isLatest"}),
        #"Expanded annotations" = Table.ExpandListColumn(#"Expanded Column1", "annotations")
    in
      #"Expanded annotations"