Example code:


      let
          ServerNames = Table.FromRows({{"xxxx.database.windows.net"},{"yyyyyy.database.windows.net"}},{"ServerName"}),
          #"Added Custom" = Table.AddColumn(#"ServerNames", "Data", each LoadSqlData([ServerName],"TableName")),
          ExpandedData = Table.Combine(#"Added Custom"[Data])
      in
          ExpandedData
