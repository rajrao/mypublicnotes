No easy way available. Just have to reorder:

          ColumnNames=Table.ColumnNames(#"SourceTable"),
          ReorderedList = List.Combine({{List.Last(ColumnNames)},List.FirstN(Table.ColumnNames(#"Added Custom"),List.Count(ColumnNames)-1)}),
          Result = Table.ReorderColumns(#"SourceTable",ReorderedList)
      in
          #"Result"
