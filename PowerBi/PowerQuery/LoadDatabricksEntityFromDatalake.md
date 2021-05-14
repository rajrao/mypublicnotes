This code represents a function that can be utilized in PowerQuery M to load a dataframe that was saved in Databricks utilizing the partition functionality.

It depends on a parameter being defined called **datalake** which should be defined in your dataset with its data pointing to Datalake with the following format: https://xxxx.dfs.core.windows.net/container/

The entity should have been written out in databricks with a command similar to this:

```
spark.conf.set("spark.sql.sources.partitionOverwriteMode","dynamic")
myDataFrame.write.mode("overwrite").partitionBy("year","month","day").parquet(pathPrefix)
```

```
let
        //  datalake (Parameter) = "https://xxx.dfs.core.windows.net/containerName/", folder = "temp/", entity = "entityFolderName", extension = ".parquet",
        Source = (folder,entity, extension) => 
        let
            Source = AzureStorage.DataLake(datalake),
            path = datalake&folder&entity&"/",
             #"Lowercased Text" = Table.TransformColumns(Source,{{"Folder Path", Text.Lower, type text}}),
            #"Filtered Rows1" = Table.SelectRows(#"Lowercased Text", each (Text.Contains([Folder Path],path,Comparer.OrdinalIgnoreCase))),
            #"Filtered Rows" = Table.SelectRows(#"Filtered Rows1", each ([Extension] = extension)),
            #"Removed Columns" = Table.RemoveColumns(#"Filtered Rows",{"Date accessed", "Date modified", "Date created", "Attributes", "Extension", "Name"}),
            #"keep only entity subfolder path" = Table.ReplaceValue(#"Removed Columns",Text.Lower(path),"",Replacer.ReplaceText,{"Folder Path"}),
            #"Uppercased Text" = Table.TransformColumns(#"keep only entity subfolder path",{{"Folder Path", Text.Upper, type text}}),
            #"Split Column by Delimiter" = Table.SplitColumn(#"Uppercased Text", "Folder Path", Splitter.SplitTextByDelimiter("/", QuoteStyle.Csv), {"Folder Path.1", "Folder Path.2", "Folder Path.3", "Folder Path.4"}),
            #"Changed Type" = Table.TransformColumnTypes(#"Split Column by Delimiter",{{"Folder Path.1", type text}, {"Folder Path.2", type text}, {"Folder Path.3", type text}, {"Folder Path.4", type text}}),
            #"Renamed Columns" = Table.RenameColumns(#"Changed Type",{{"Folder Path.1", "Year"}, {"Folder Path.2", "Month"}, {"Folder Path.3", "Day"}}),
            #"Removed Columns1" = Table.RemoveColumns(#"Renamed Columns",{"Folder Path.4"}),
            #"fix year=" = Table.ReplaceValue(#"Removed Columns1","YEAR%3D","",Replacer.ReplaceText,{"Year"}),
            #"fix month=" = Table.ReplaceValue(#"fix year=","MONTH%3D","",Replacer.ReplaceText,{"Month"}),
            #"fix day=" = Table.ReplaceValue(#"fix month=","DAY%3D","",Replacer.ReplaceText,{"Day"}),
            #"combine as yyyymmdd" = Table.CombineColumns(#"fix day=",{"Year", "Month", "Day"},Combiner.CombineTextByDelimiter("", QuoteStyle.None),"Date"),
            #"convert to date" = Table.TransformColumnTypes(#"combine as yyyymmdd",{{"Date", type date}}),
            #"convert to datetime" = Table.TransformColumnTypes(#"convert to date",{{"Date", type datetime}})
        in
            #"convert to datetime"
in
    Source
```
