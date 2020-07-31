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
    
