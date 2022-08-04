Shows how to reference data in a table by its column index.

```
Record.Field(_, Table.ColumnNames(#"SourceTable"){1})
```

Example: Removes rows with null or empty text in 2nd column of SourceTable

```
= Table.SelectRows(#"SourceTable", each Record.Field(_, Table.ColumnNames(#"SourceTable"){1}) <> null and Record.Field(_, Table.ColumnNames(#"SourceTable"){1}) <> "")
```
