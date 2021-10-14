This shows you how to dynamically pull Form data from Microsoft Forms into PowerBi.
For this to work you need the FormId. The easiest way to get the form id is to click share, copy the URL and extract everything after ?id=
eg: https://forms.office.com/Pages/ResponsePage.aspx?id=**THIS-IS-THE-FORMID**


Steps:
1. Create a blank query and enter the following in Advanced Query Editor
  ```
  // GetFormsData
  (formId,optional minId, optional maxId) =>
  let
     minResponseId = if minId = null then "1" else Text.From(minId),
     maxResponseId = if maxId = null then "5000" else Text.From(maxId),
     relativeFormUri = "?formid=" & formId & "&timezoneOffset=0&__TimezoneId=UTC&minResponseId=" & minResponseId & "&maxResponseId=" & maxResponseId,
     webContents =  Web.Contents("https://forms.office.com/formapi/DownloadExcelFile.ashx", [RelativePath = relativeFormUri]),
     Source = Excel.Workbook(webContents, null, true),
     TableData = Source{[Item="Table1",Kind="Table"]}[Data]
  in
      TableData
  ```
2. Invoke the function and replace "ENTER FORM ID HERE" with the formId.
  ```
  // Invoked Function
  let
      Source = GetFormsData("ENTER FORM ID HERE"),
      #"Changed Type" = Table.TransformColumnTypes(Source,{{"ID", Int64.Type}, {"Start time", type datetime}, {"Completion time", type datetime}, {"Email", type text}, {"Name", type text}, {"Best Starwars movie was", type text}}),
      #"Added Custom" = Table.AddColumn(#"Changed Type", "Custom", each DateTimeZone.ToLocal(DateTime.AddZone([Start time],0)))
  in
      #"Added Custom"
  ```    
