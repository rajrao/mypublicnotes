Sometimes you need to update the names of multiple columns at once in a similar way (eg: replace "_" with " ").
The following code can be used in the AdvancedEditor to perform that.

    = Table.TransformColumnNames(#"Promoted Headers", (columnName as text) as text => Text.Replace(columnName, "_", " "))
