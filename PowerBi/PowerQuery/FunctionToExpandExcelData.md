```
//Entity
let
  Source = SharePoint.Files("https://mysharepoint.sharepoint.com/sites/mysite", [ApiVersion = 15]),
  #"Filtered rows" = Table.SelectRows(Source, each Text.Contains([Folder Path], "/subfoldername/")),
  #"Filtered rows 1" = Table.SelectRows(#"Filtered rows", each [Name] = "excelfile.xlsx"),
  #"Removed other columns" = Table.SelectColumns(#"Filtered rows 1", {"Content", "Name", "Date modified"}),
  #"Added custom" = Table.AddColumn(#"Removed other columns", "Data", each ExpandExcelData(#"Removed other columns"{0}[Content],"Page 1")),
  #"Removed columns" = Table.RemoveColumns(#"Added custom", {"Content"}),
  #"Renamed columns" = Table.RenameColumns(#"Removed columns", {{"Name", "FileName"}, {"Date modified", "FileModifiedDate"}})
  //expand "Data" column
  //detect data types
in
  #"Renamed columns"

// ExpandExcelData function
(parameter1,parameter2) => let
  #"Imported Excel workbook" = Excel.Workbook(parameter1, null, true),
  #"Navigation 1" = #"Imported Excel workbook"{[Item = parameter2, Kind = "Sheet"]}[Data],
  #"Promoted headers" = Table.PromoteHeaders(#"Navigation 1", [PromoteAllScalars = true])
in
  #"Promoted headers"
```  
