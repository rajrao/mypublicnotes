This is especially useful for retrieving data from Dynamics CRM (PowerPlatform) using ODATA

    let
        Source = OData.Feed("https://myOrg.crm.dynamics.com/api/data/v9.1/opportunities?$select=name,opportunityid,statecode&$filter=fieldXyz ne null", null, [Implementation="2.0",IncludeAnnotations="*"]),
        #"Added Custom" = Table.AddColumn(Source, "StateCodeLabel", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue])
    in
        #"Added Custom"
        

Note: If your field can have null values, you use the following code so that it doesnt fail (question mark at the end): Value.Metadata([fieldName])[OData.Community.Display.V1.FormattedValue]?) {This is the optional selector operator, see [MsDoc](https://docs.microsoft.com/en-us/powerquery-m/m-spec-operators#item-access)}
