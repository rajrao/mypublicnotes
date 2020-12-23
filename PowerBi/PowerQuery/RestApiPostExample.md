The following demonstrated how to perform Post to a url with custom headers, etc. This example is based on fetching data from Azure's manamagement rest api, but could easily be modified to perform a post against any URL.

Note: *If you get a **Web.Content doesnt support authentication**, then you will have to go into **datasource settings** and mark the urls as using anonymous auth.*


    let
      //Set variables for authenticating to Azure using Service Principal and making API request
      tenantID = "<tenantid>",
      subscriptionId = "<subid>",
      resourceGroupName = "<rgName>",
      factoryName = "<factoryName>",
      apiVersion = "2018-06-01",
      appId = "<clientId>", //this service principal will need "Data Factory Contributor" role (not sure if there is a more limited role than that available for this
      clientSecrets = "<clientSecret>",
      uri = "tenantID & "/oauth2/token",
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
        Web.Contents("https://login.microsoftonline.com/", [RelativePath = uri, Headers = authHeaders, Content = Text.ToBinary(authQueryString)])
      ),
      token = auth[access_token],
      //Build request URL & Body using variables
      url
        = subscriptionId & "/resourceGroups/"
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
        Web.Contents("https://management.azure.com/subscriptions/", [RelativePath = url, Headers = reqHeaders, Content = Text.ToBinary(reqBody)])
      ),
        value = result[value],
        #"Converted to Table" = Table.FromList(value, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
        #"Expanded Column1" = Table.ExpandRecordColumn(#"Converted to Table", "Column1", {"id", "runId", "debugRunId", "runGroupId", "pipelineName", "parameters", "invokedBy", "runStart", "runEnd", "durationInMs", "status", "message", "lastUpdated", "annotations", "runDimension", "isLatest"}, {"id", "runId", "debugRunId", "runGroupId", "pipelineName", "parameters", "invokedBy", "runStart", "runEnd", "durationInMs", "status", "message", "lastUpdated", "annotations", "runDimension", "isLatest"}),
        #"Expanded annotations" = Table.ExpandListColumn(#"Expanded Column1", "annotations")
    in
      #"Expanded annotations"


based on example from: https://www.bluegranite.com/blog/monitoring-azure-data-factory-v2-using-power-bi
