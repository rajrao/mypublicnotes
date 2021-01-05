Example code:


      let
          ServerNames = Table.FromRows({{"xxxx.database.windows.net"},{"yyyyyy.database.windows.net"}},{"ServerName"}),
          #"Added Custom" = Table.AddColumn(#"ServerNames", "Data", each LoadSqlData([ServerName],"TableName")),
          ExpandedData = Table.Combine(#"Added Custom"[Data])
      in
          ExpandedData

Where **LoadSqlData** is a function with the following code, but could be anything you wish to call:

       let
          Source = (serverName as text, dbName as text, schema as text tableName as text) => let
              Source = Sql.Databases(serverName),
              Db = Source{[Name=dbName]}[Data],
              data = Db{[Schema=schema,Item=tableName]}[Data]
          in
              data
      in
          Source
