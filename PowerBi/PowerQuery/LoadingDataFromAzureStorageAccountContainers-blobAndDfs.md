Loading data from an azure blob.

Notes:

1. I use blob, because using the DFS endpoint leads to all sorts of permissions issues and with blob, you can use the key.
2. But with DFS, you can use your Azure AD creds to authenticate.
3. I have found no performance difference between using the blobs and the DFS.
4. This line is important **Source = AzureStorage.Blobs(DLPath),** and if you have many files to load data from, then this is the best way to do it! 
    The reason is that authentication occurs at level of the DLPath. By keeping it consistent, you will have to authenticate just once at that level.


          let
            FileName = "xyz.csv",
            FileFolder = "abc defg/",
            DataLakePath = "https://myAzStorageAccount.blob.core.windows.net/container/",
            DataLakeSource = FileFolder,
            Source = AzureStorage.Blobs(DataLakePath),
            #"GetFileContent" = Source{[#"Folder Path"=DataLakePath,Name=FileFolder&FileName]}[Content],
            #"Imported CSV" = Csv.Document(GetFileContent,[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
            #"Promoted Headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars=true])
          in
            #"Promoted Headers"
            

Using DFS endpoint: (


          let
            FileName = "xyz.csv",
            FileFolder = "abc%20defg/",
            DataLakePath = "https://myAzStorageAccount.dfs.core.windows.net/container/",
            DataLakeSource = FileFolder,
            Source = AzureStorage.DataLake(DataLakePath),
            #"GetFileContent" = Source{[#"Folder Path"=DataLakePath&FileFolder,Name=FileName]}[Content],
            #"Imported CSV" = Csv.Document(GetFileContent,[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
            #"Promoted Headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars=true])
          in
            #"Promoted Headers"
            
            
Using Parquet:

            
          let
            FileName = "xyz.parquet",
            FileFolder = "abc defg/",
            DataLakePath = "https://myAzStorageAccount.blob.core.windows.net/container/",
            DataLakeSource = FileFolder,
            Source = AzureStorage.Blobs(DataLakePath),
            #"GetFileContent" = #"Source"{[#"Folder Path"=DataLakePath,Name=FileFolder&FileName]}[Content],
            #"Imported data" = Parquet.Document(#"GetFileContent")
          in
            #"Imported data"
            
