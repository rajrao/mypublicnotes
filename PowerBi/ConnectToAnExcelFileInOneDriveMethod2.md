You can follow the steps outlined below, or alternatively, you can copy the code at the bottom of this page and update the variables and use it as is.

1. Click on "Get Data" and pick the "Sharepoint Folder" option and click connect.
2. Enter the site URL which will be of the form: "https://yourOrg.sharepoint.com/sites/YourExcelSite/" (even if your file is in a subfolder, the path you need to enter here will end at "YourExcelSite").
3. For Sign On screen, pick "Microsoft Account" and under "Select which level to apply these settings", pick the lowest level you can.In my case, that will be "https://yourOrg.sharepoint.com/sites/YourExcelSite/"
4. Click Connect.
5. Next click on "Transform Data"
6. You should see "Content", "Name" (the file name) and "Folder Path". 
7. Filter to the folder path and/or file name, so you see the file you want to ingest.
8. At this point you should see just the file you want to ingest.
9. Click on the "Binary" word. When you do this, PBI will detect that its an excel file and open it up
10. At this point you should see all the sheets and tables in your file. Click on the sheet or table you wish to ingest.
11. If you picked a "Sheet" you will likely wont to promote your first row to headers ("Use First Row as Headers"). If you picked "Table", then the headers should automatically get picked for you.


These steps should look like this:

Update the following values in the script to match your file's location: **{myOrg},{MySiteName},{SubFolder1},{SubFolder2},{fileName}**

When using this code, you will need to adjust "Load Sheet 1" and the following step based on the sheet or table you are importing. 

```
let
    siteUrl = "https://{myOrg}.sharepoint.com/sites/{MySiteName}/",
    folderPath = siteUrl & "Shared Documents/{SubFolder1}/{SubFolder2}/",
    excelFileName = "{fileName}.xlsx",
    Source = SharePoint.Files(siteUrl, [ApiVersion = 15]),
    #"Filtered Rows" = Table.SelectRows(Source, each ([Folder Path] = folderPath and [Name] = excelFileName)),
    #"Load Excel File Binary" = #"Filtered Rows"{[Name=excelFileName,#"Folder Path"=folderPath]}[Content],
    //After the following step, you should import the sheet or table you need. You do this by directly clicking on "Table"
    #"Load Binary as Excel File" = Excel.Workbook(#"Load Excel File Binary")
in
    #"Load Binary as Excel File"
```
