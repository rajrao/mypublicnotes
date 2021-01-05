Example code:


      let
          ServerNames = Table.FromRows({{"xxxx.database.windows.net"},{"yyyyyy.database.windows.net"}},{"ServerName"}),
          #"Added Custom" = Table.AddColumn(#"ServerNames", "Data", each LoadSqlData([ServerName],"TableName")),
          Custom1 = Table.Combine(#"Added Custom"[Data])
      in
          Custom1
