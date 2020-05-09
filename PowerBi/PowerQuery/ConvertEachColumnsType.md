
      = Table.TransformColumnTypes(
            Source,
            List.Transform(
                List.RemoveFirstN(
                    Table.ColumnNames(Source),
                    2
                ),
            each {_, type number}
            )
        )

[via](https://stackoverflow.com/a/52082067/44815)
