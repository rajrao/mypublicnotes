This is especially useful for retrieving data from Dynamics CRM (PowerPlatform) using ODATA

    let
        Source = OData.Feed("https://myOrg.crm.dynamics.com/api/data/v9.1/opportunities?$select=name,opportunityid,statecode&$filter=fieldXyz ne null", null, [Implementation="2.0",IncludeAnnotations="*"]),
        #"Added Custom" = Table.AddColumn(Source, "StateCodeLabel", each Value.Metadata([statecode])[OData.Community.Display.V1.FormattedValue]?)
    in
        #"Added Custom"
        
The ? in "[OData.Community.Display.V1.FormattedValue]**?**" allows the code to continue even if a formatted value is not returned.
