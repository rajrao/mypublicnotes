This technique is useful for removing duplicates or for adding a grouped index (a row number based on some sort of grouping). Because this allows you to get rid of duplicate rows based on a specific sort order, its especially useful for tables you will end up using as dimensions (1 side of a 1:n).

    1. Sort the table by the columns you want grouped. Use: 
    
            Table.Sort(InputTable,{{"Column1", Order.Ascending},{"Column2", Order.Descending}})
        
        Normally the first column will be an ID column and the 2nd column something like date, so that you can pick the latest
    
    2. Use Transform >> Group By and group the sorted data.
            
            For grouping, you will use the first column from (1)
            
            New Column Name: Rows
            
            Operation: All Rows
           
            
    3. Via the advanced editor, add the following formula to index each of the tables: (it adds a index starting at 1, incrementing by 1, per row)
        
            #"Indexed" = Table.TransformColumns(#"Grouped Rows", {{"Rows", each Table.AddIndexColumn( _, "GroupIndex", 1, 1)}}),
            
    4. Expand the Rows column to expand all the columns except the ones used in the grouping.
    
    5. If your end goal is to keep only one of the records, filter by GroupIndex = 1.
    
    
    
