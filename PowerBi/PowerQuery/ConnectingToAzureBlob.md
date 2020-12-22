Loading data from an azure blob.

Notes:

1. I use blob, because using the DFS endpoint leads to all sorts of permissions issues.
2. This line is important **Source = AzureStorage.DataLake(DLPath),** and if you have many files to load data from, then this is the best way to do it! 
    The reason is that authentication occurs at level of the DLPath. By keeping it consistent, you will have to authenticate just once at that level.


          let
            FileName = "xyz.csv",
            FileFolder = "abc/",
            DataLakePath = "https://myAzStorageAccount.blob.core.windows.net/container/",
            DataLakeSource = DataLakePath  & FileFolder,
            Source = AzureStorage.DataLake(DataLakePath),
            #"GetFileContent" = Source{[#"Folder Path"=DataLakeSource,Name=FileName]}[Content],
            #"Imported CSV" = Csv.Document(GetFileContent,[Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
            #"Promoted Headers" = Table.PromoteHeaders(#"Imported CSV", [PromoteAllScalars=true])
          in
            #"Promoted Headers"
