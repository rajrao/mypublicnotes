1. Adding a grouped index:
  To add an index by some sort of grouping:
    1. Sort the table by the columns you want grouped. Use: 
    
            Table.Sort(InputTable,{{"Column1", Order.Ascending},{"Column2", Order.Descending}})
    2. Use Transform >> Group By and group the sorted data.
        Call the output (New Column Name) Rows, Operation: Rows.
    3. Via the advanced editor, add the following formula to index each of the tables: (it adds a index starting at 1, incrementing by 1, per row)
        
            Indexed = Table.TransformColumns(#"Grouped Rows", {{"Rows", each Table.AddIndexColumn( _, "GroupIndex", 1, 1)}}),
    4. Expand the Rows column to expand all the columns except the ones used in the grouping.
    
    
    
