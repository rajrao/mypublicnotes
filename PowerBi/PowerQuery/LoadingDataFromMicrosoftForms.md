This shows you how to dynamically pull Form data from Microsoft Forms into PowerBi.
For this to work you need the FormId. The easiest way to get the form id is to click share, copy the URL and extract everything after ?id=
eg: [https://forms.office.com/Pages/ResponsePage.aspx?id=**THIS-IS-THE-FORMID**]


**Steps:**
1. Create a blank query and enter the code from below in Advanced Query Editor. Click done. Rename the query as **"GetFormsData"**
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
2. Create another blank query. Add the following code to that query, which will invoke the function GetFormsData. Replace "ENTER FORM ID HERE" with the formId you retrieved at the top of this document. Repeat this step for every form that you have.
  
  ```
  // Invoked Function
  let
      Source = GetFormsData("ENTER FORM ID HERE"),
      #"StartTime Local" = Table.AddColumn(Source, "Start Time Local", each DateTimeZone.ToLocal(DateTime.AddZone([Start time],0))),
      #"CompletionTime Local" = Table.AddColumn(#"StartTime Local", "Completion Time Local", each DateTimeZone.ToLocal(DateTime.AddZone([Completion time],0))),
      #"Changed Type" = Table.TransformColumnTypes(#"CompletionTime Local",{{"ID", Int64.Type}, {"Start time", type datetime}, {"Completion time", type datetime}, {"Start Time Local", type datetimezone}, {"Completion Time Local", type datetimezone}})
  in
      #"Changed Type"
  ```    
