
      = Table.TransformColumnTypes(
            #"SourceTable",
            List.Transform(
                List.RemoveFirstN(
                    Table.ColumnNames(#"SourceTable"),
                    2
                ),
            each {_, type number}
            )
        )

[via Stackoverflow](https://stackoverflow.com/a/52082067/44815)
