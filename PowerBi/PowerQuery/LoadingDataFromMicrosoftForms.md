The best way to capture Microsoft Forms data is by creating your form from within a Microsoft Sharepoint Site. When you do this, the form will automatically create an excel file within the site using the "Forms for Excel" functionality. This will allow you to use simple excel integration instead of any of the complicated stuff outlined below.

<img src="https://user-images.githubusercontent.com/1643325/162518404-bd1857f4-ca55-4c6e-86ce-dc0316a9e24f.png" width="200" />

To access the above option, click on new from within a sharepoint site to which you have write permissions. Once the form is created, you will find an excel file in the sharepoint site with the same name as the form. This excel file will have the latest data from the form responses.

Once you have located the excel file, please follow the instructions here: https://github.com/rajrao/mypublicnotes/blob/master/PowerBi/ConnectToAnExcelFileInOneDrive.md

----
**Please ignore the following instructions. They work but are harder. Instead use the one "Connect to an Excel File in One Drive" linked above.**

If "Forms for Excel is not an option", then the following shows you how to dynamically pull Form data from Microsoft Forms into PowerBi.
For this to work you need the FormId. The easiest way to get the form id is to click share, copy the URL and extract everything after ?id=
eg: [https://forms.office.com/Pages/ResponsePage.aspx?id=**THIS-IS-THE-FORMID**]

**Steps**
1. Create a blank query and enter the code from below in Advanced Query Editor. Update "FORM_ID_HERE" with actual form id you retrieved above. Click done.
```
  let
      webContents =  Web.Contents("https://forms.office.com/formapi/DownloadExcelFile.ashx?formid=FORM_ID_HERE&timezoneOffset=0&__TimezoneId=UTC&minResponseId=1&maxResponseId=5000"),
      Source = Excel.Workbook(webContents, null, true),
      TableData = Source{[Item="Table1",Kind="Table"]}[Data],
      #"StartTime Local" = Table.AddColumn(TableData, "Start Time Local", each DateTimeZone.ToLocal(DateTime.AddZone([Start time],0))),
      #"CompletionTime Local" = Table.AddColumn(#"StartTime Local", "Completion Time Local", each DateTimeZone.ToLocal(DateTime.AddZone([Completion time],0))),
      #"Changed Type" = Table.TransformColumnTypes(#"CompletionTime Local",{{"ID", Int64.Type}, {"Start time", type datetime}, {"Completion time", type datetime}, {"Start Time Local", type datetimezone}, {"Completion Time Local", type datetimezone}})
  in
      #"Changed Type"
```

---

**Old Steps:** *dont use if you want to refresh in PowerBi.com*
This method will work locally. But, doesnt quite work on Powerbi.com, as the service doesnt like queries that get created on the fly and it cant authenticate against the main url as the actual form is part of the relative url.
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
