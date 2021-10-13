
```
let
    //update the varaibles in this section:
    DataflowWorkspace = "{Workspace name here}",
    DataflowName = "{dataflow name here}",
    EntityName = "{entity name here}",
    //no changes here. this section loads the data
    Source = PowerBI.Dataflows(null),
    #"Filtered to Workspace" = Table.SelectRows(Source, each [workspaceName] = DataflowWorkspace),
    #"Removed all but Workspace Data" = Table.SelectColumns(#"Filtered to Workspace",{"Data"}),
    #"Expanded Workspace Metadata" = #"Removed all but Workspace Data"{0}[Data],
    #"Expanded Data" = Table.ExpandTableColumn(#"Expanded Workspace Metadata", "Data", {"entity", "Data"}, {"Data.entity", "Data.Data"}),
    #"Filtered Rows" = Table.SelectRows(#"Expanded Data", each [Data.entity] = EntityName),
    #"Return Dataflow Data" = #"Filtered Rows"{0}[Data.Data]
in 
  #"Return Dataflow Data"
  
  ```
