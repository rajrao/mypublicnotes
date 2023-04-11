To display sharepoint images in a PowerBi report, you need to first upload all your images to a location that is accessible by the users of your report.

There are 2 options for uploading your images:
1. Create a document library and provide access to that document library to all the users of your report or
2. Create a folder in an existing document library and provide access to all your report users to that folder.

After you have uploaded the images to sharepoint, you just need the URL of the images to add them into your report. The URL is of the format: https://yourcompany.sharepoint.com/sites/YourSharePointSiteName/YourImageFolderName/YourSubFolderName/FileName.png

You will need to get the values for yourcompany, YourSharePointSiteName, YourImageFolderName, YourSubFolderName (optional) for use later on. You can pick it by looking at the URL in your address bar.

You have 2 options for the image URLs, you can hard code them into your report, or you can use the following transformation in PowerQueryEditor:

1. Go into PowerQueryEditor (Transform Data)
2. Click on "New Source" >> "Blank Query"
3. With the new query selected, click on "Advanced Editor"
4. Paste the following code into the editor:
```
   let
    Source = SharePoint.Files("https://yourCompany.sharepoint.com/sites/YourSiteName", [ApiVersion = 15]),
    #"Filtered Rows" = Table.SelectRows(Source, each [Folder Path] = "https://yourCompany.sharepoint.com/sites/YourSiteName/YourFolder/"),
    #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Content", "Extension", "Date accessed", "Date modified", "Date created", "Attributes"}),
    #"Duplicated Column" = Table.DuplicateColumn(#"Removed Columns", "Name", "Name - Copy"),
    #"Merged Columns" = Table.CombineColumns(#"Duplicated Column",{"Folder Path", "Name - Copy"},Combiner.CombineTextByDelimiter("", QuoteStyle.None),"ImageUrl")
  in
    #"Merged Columns"
```

6. Update the text yourCompany, YourSiteName, YourFolder in the above code and use the correct names for your case.
7. Click on "Done"
8. Your query will 2 columns "Name" and "ImageUrl"
9. Close & Apply your transformation.
10. Click on ImageUrl field of the new table and in your "Column Tools" toolbar, set the "Data Category" to "Image URL"

![image](https://user-images.githubusercontent.com/1643325/231216829-44420d39-db09-491b-b243-1fc2d286c3b4.png)

11. If you add the Name and ImageUrl to a table, it will look broken!

![image](https://user-images.githubusercontent.com/1643325/231217004-e5391b3f-6520-469d-8019-6c5eba1f2c39.png)

12. Publish your report to PowerBi.com
13. In powerbi.com the report should render the images

![image](https://user-images.githubusercontent.com/1643325/231217768-90c4795e-cf92-4464-b9a7-80b1c6f90261.png)

Now that you have tested displaying Sharepoint images in your report, you can use the above links in your report, by connecting your image your table to your data (eg: you could upload the files with the name of employees or categories and join the data to your data-table that has employee names or categories).
