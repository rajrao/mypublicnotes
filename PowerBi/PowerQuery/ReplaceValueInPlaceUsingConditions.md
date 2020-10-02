In place update of a column using logic based on other columns in the table


    = Table.ReplaceValue(#"Input Table",
                              each [ColumnToEvaluate],
                              each if ([ColumnToEvaluate] = null) then [ValueFromOtherColumn] else [ColumnToEvaluate],
                              Replacer.ReplaceValue,
                              {"ColumnToEvaluate"})
    
Example 2
    
    = Table.ReplaceValue(#"Input Table",each [ColumnToEvaluate], 
                             each Date.AddYears([ColumnToEvaluate],-1), 
                             Replacer.ReplaceValue,
                             {"ColumnToEvaluate"})
    
Example 3

- Input table: #Changed Type 1"
- Column: "Date - Copy"
- Function: remove text
    
      = Table.ReplaceValue(#"Changed Type1",each [#"Date - Copy"], 
                            each Text.RemoveRange([#"Date - Copy"],10,14), 
                            Replacer.ReplaceValue, 
                            {"Date - Copy"} )
