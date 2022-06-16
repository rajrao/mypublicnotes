```
// Start Year
2022 meta [IsParameterQuery=true, Type="Number", IsParameterQueryRequired=true]

// Fiscal Start Month
4 meta [IsParameterQuery=true, Type="Number", IsParameterQueryRequired=true]

// Fiscal Calendar
let
Date = let
  Source = List.Dates,
  FiscalMonthCalc = 12-#"Fiscal Start Month",

  // 1. Uncomment this line if you want to get your end date being Today's Date of the Refresh
  //#"Invoked FunctionSource" = Source(#date(#"Start Year", 1, 1), Duration.Days(DateTime.Date(DateTime.FixedLocalNow()) - #date(#"Start Year",1,1)), #duration(1, 0, 1, 0)),

  // 2. Uncomment this line below if you want your end date to be 4 years into the future
  #"Invoked FunctionSource" = Source(#date(#"Start Year", 1, 1), Duration.Days(DateTime.Date(Date.AddDays(Date.EndOfYear(Date.AddYears(DateTime.FixedLocalNow(),+4)),-1)) - #date(#"Start Year",1,1)), #duration(1, 0, 1, 0)),

  // 3. Uncomment this line if you want to get your end date being the Parameter called "End Year"
  //#"Invoked FunctionSource" = Source(#date(#"Start Year", 1, 1), Duration.Days(#date(#"End", 12, 30) - #date(#"Start Year",1,1)), #duration(1, 0, 1, 0)),

  #"Table from List" = Table.FromList(#"Invoked FunctionSource", Splitter.SplitByNothing(), null, null, ExtraValues.Error),
  #"Added Index" = Table.AddIndexColumn(#"Table from List", "Index", 1, 1),
  #"Renamed Columns" = Table.RenameColumns(#"Added Index",{{"Column1", "Date"}}),
  #"Added Custom" = Table.AddColumn(#"Renamed Columns", "Year", each Date.Year([Date])),
  #"Added Custom1" = Table.AddColumn(#"Added Custom", "Month Number", each Date.Month([Date])),
  #"Added Custom2" = Table.AddColumn(#"Added Custom1", "Day", each Date.Day([Date])),
  #"Added Custom3" = Table.AddColumn(#"Added Custom2", "Day Name", each Date.ToText([Date],"ddd")),
  #"Added Custom4" = Table.AddColumn(#"Added Custom3", "Month Name", each Date.ToText([Date],"MMM")),
  #"Reordered Columns" = Table.ReorderColumns(#"Added Custom4",{"Date", "Index", "Year", "Month Number", "Month Name", "Day", "Day Name"}),
  #"Added Custom5" = Table.AddColumn(#"Reordered Columns", "Quarter Number", each Date.QuarterOfYear([Date])),
  #"Duplicated Column" = Table.DuplicateColumn(#"Added Custom5", "Year", "Copy of Year"),
  #"Renamed Columns1" = Table.RenameColumns(#"Duplicated Column",{{"Copy of Year", "Short Year"}}),
  #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns1",{{"Short Year", type text}}),
  #"Split Column by Position" = Table.SplitColumn(#"Changed Type","Short Year",Splitter.SplitTextByRepeatedLengths(2),{"Short Year.1", "Short Year.2"}),
  #"Changed Type1" = Table.TransformColumnTypes(#"Split Column by Position",{{"Short Year.1", Int64.Type}, {"Short Year.2", Int64.Type}}),
  #"Removed Columns" = Table.RemoveColumns(#"Changed Type1",{"Short Year.1"}),
  #"Renamed Columns2" = Table.RenameColumns(#"Removed Columns",{{"Short Year.2", "Short Year"}}),
  #"Added Custom6" = Table.AddColumn(#"Renamed Columns2", "Quarter Year", each Number.ToText([Short Year]) & "Q" & Number.ToText([Quarter Number],"00")),
  #"Reordered Columns1" = Table.ReorderColumns(#"Added Custom6",{"Index", "Date", "Day", "Day Name", "Month Number", "Month Name", "Quarter Number", "Quarter Year", "Short Year", "Year"}),
  #"Changed Type2" = Table.TransformColumnTypes(#"Reordered Columns1",{{"Date", type date}, {"Day", Int64.Type}, {"Index", Int64.Type}, {"Month Number", Int64.Type}, {"Quarter Number", Int64.Type}, {"Month Name", type text}, {"Quarter Year", type text}, {"Year", Int64.Type}}),
  #"Added Conditional Column" = Table.AddColumn(#"Changed Type2", "Fiscal Year", each if [Month Number] < #"Fiscal Start Month" then [Year]-1 else [Year] ),
  #"Added Conditional Column1" = Table.AddColumn(#"Added Conditional Column", "Fiscal Month", each if [Month Number] < #"Fiscal Start Month" then [Month Name] else [Month Name] ),
  #"Added Custom7" = Table.AddColumn(#"Added Conditional Column1", "Fiscal Month Sort Order", each Number.Mod(Date.Month([Date])+FiscalMonthCalc ,12)+1),
  #"Added Conditional Column3" = Table.AddColumn(#"Added Custom7", "Fiscal Quarter", each if [Fiscal Month Sort Order] >= 1 and [Fiscal Month Sort Order] <= 3 then "Q1" 
   else if [Fiscal Month Sort Order] >= 4 and [Fiscal Month Sort Order] <= 6 then "Q2" 
   else if [Fiscal Month Sort Order] >= 7 and [Fiscal Month Sort Order] <= 9 then "Q3" 
   else if [Fiscal Month Sort Order] >= 10 and [Fiscal Month Sort Order] <= 12 then "Q4" 
   else "Q Unknown" ),
  #"Added Conditional Column4" = Table.AddColumn(#"Added Conditional Column3", "Fiscal Quarter Sort Number", each if [Fiscal Month Sort Order] >= 1 and [Fiscal Month Sort Order] <= 3 then "1" 
   else if [Fiscal Month Sort Order] >= 4 and [Fiscal Month Sort Order] <= 6 then "2" 
   else if [Fiscal Month Sort Order] >= 7 and [Fiscal Month Sort Order] <= 9 then "3" 
   else if [Fiscal Month Sort Order] >= 10 and [Fiscal Month Sort Order] <= 12 then "4" 
   else "Q Unknown" ),
  #"Changed Type3" = Table.TransformColumnTypes(#"Added Conditional Column4",{{"Fiscal Quarter Sort Number", Int64.Type}, {"Fiscal Month Sort Order", Int64.Type}, {"Fiscal Year", Int64.Type}}),
  #"Renamed Columns3" = Table.RenameColumns(#"Changed Type3",{{"Date", "Calendar Date"}, {"Month Number", "Calendar Month Number"}, {"Month Name", "Calendar Month Name"}, {"Quarter Number", "Calendar Quarter Number"}, {"Quarter Year", "Calendar Quarter Year"}, {"Short Year", "Calendar Short Year"}, {"Year", "Calendar Year"}})

  in
  #"Renamed Columns3",
  #"Duplicated Column" = Table.DuplicateColumn(Date, "Calendar Date", "Calendar Date - Copy"),
  #"Calculated Week of Year" = Table.TransformColumns(#"Duplicated Column",{{"Calendar Date - Copy", Date.WeekOfYear}}),
  #"Renamed Columns" = Table.RenameColumns(#"Calculated Week of Year",{{"Calendar Date - Copy", "Week Number of Year"}}),
  #"Duplicated Column1" = Table.DuplicateColumn(#"Renamed Columns", "Calendar Date", "Calendar Date - Copy"),
  #"Calculated Week of Month" = Table.TransformColumns(#"Duplicated Column1",{{"Calendar Date - Copy", Date.WeekOfMonth}}),
  #"Renamed Columns1" = Table.RenameColumns(#"Calculated Week of Month",{{"Calendar Date - Copy", "Week Number of Month"}}),
      #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns1",{{"Calendar Date", type date}}),
      #"Added Custom" = Table.AddColumn(#"Changed Type", "Fiscal Year Quarter", each Number.ToText([Fiscal Year]) & " - " & [Fiscal Quarter]),
      #"Added Conditional Column" = Table.AddColumn(#"Added Custom", "Weekend", each if [Day Name] = "Sun" then "Y" else if [Day Name] = "Sat" then "Y" else "N")
in
    #"Added Conditional Column"
```    
