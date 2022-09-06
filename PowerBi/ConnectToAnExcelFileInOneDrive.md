1. Upload the file to your organization's onedrive/sharepoint folder.

2. Get the link to the file in sharepoint:
   There are 2 ways to get the link to the file:
   1. **The easy way** (using Excel desktop - added 2022-09-06):
      1. Open the file from Sharepoint in Excel Desktop.

      ![image](https://user-images.githubusercontent.com/1643325/188721106-0c7a3dda-f4c0-4092-802a-c4e3a38690a2.png)
      
      2. Go to File >> Info and then Click Copy Path.
      
      ![image](https://user-images.githubusercontent.com/1643325/188721357-6ac19bbc-ae1e-4fcb-8f4b-fe46cbb4aa4a.png)

   2. **The longer method** (without using Excel desktop):
      1. In OneDrive/Sharepoint, select the file.
      2. Copy the link and remove anything that shows up after the file extension. (You should choose the "People with existing access" option).
      
      ![CopyLink1](https://user-images.githubusercontent.com/1643325/78917933-d782d400-7a4c-11ea-9250-78b7011888df.png)
        
      ![CopyLink2](https://user-images.githubusercontent.com/1643325/78918067-1022ad80-7a4d-11ea-9cf2-260f47bf463f.png)
      
      3. Once you have the URL, you have to fix up the URL so that you can use it in PowerBi in such a way that PowerBi Online will be able to refresh from the file without using a gate-way. To do this, you have to remove the **`/:x:/r/`** and also any extra characters that show up at the end: (Please note that the `:x:/r` might not be in your url, in which case just make sure to clean up the trailing useless characters after the file extension).

       URL with useless characters:
       ![EditLink](https://user-images.githubusercontent.com/1643325/78918217-4d873b00-7a4d-11ea-8ac3-9112add69760.png)

       Fixed up URL
       ![EditLink2](https://user-images.githubusercontent.com/1643325/78918297-6c85cd00-7a4d-11ea-9062-6a4064a50b7b.png)
  
4. Add the file as a data-source to PowerBi desktop:
    * Choose New Source >> Web and paste the link. When you click next, it should set it up to directly bring the data from sharepoint, instead of trying to download it your machine.
    * Remove the "?web=1" from the path if it has it.
    * Crosscheck that the source is setup like this: (the key here is that it says: Web.Contents and not File.Contents.
      
           = Excel.Workbook(Web.Contents("LONG PATH TO YOUR FILE STARTING WITH HTTPS://"), null, true)
    
    * Publish your report to PBI online.

5. Update your connection information in PBI online to make sure it refreshes:
   To do this, you use OAuth2 and your credentials.
   
   ![UpdateWebCredentials](https://user-images.githubusercontent.com/1643325/78918389-96d78a80-7a4d-11ea-8747-9fe1ca47789a.png)
