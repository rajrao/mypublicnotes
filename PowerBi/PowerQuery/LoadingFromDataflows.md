
```
let
    DataflowName = "dataflowName",
    Source = PowerBI.Dataflows(null),
    #"Filtered to Workspace" = Table.SelectRows(Source, each [workspaceName] = DataflowWorkspace),
    #"Removed all but Workspace Data" = Table.SelectColumns(#"Filtered to Workspace",{"Data"}),
    #"Expanded Workspace Metadata" = #"Removed all but Workspace Data"{0}[Data],
    #"Filtered to Dataflow" = Table.SelectRows(#"Expanded Workspace Metadata", each ([dataflowName] = DataflowName)),
    #"Expanded Dataflow Metadata" = Table.ExpandTableColumn(#"Filtered to Dataflow", "Data", {"Data"}, {"Data.Data"}),
    #"Return Dataflow Data" = #"Expanded Dataflow Metadata"{0}[Data.Data]
in 
  #"Return Dataflow Data"
  
  ```
