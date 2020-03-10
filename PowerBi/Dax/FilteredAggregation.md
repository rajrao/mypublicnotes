FilteredMaxValue = CALCULATE(MAX(Table[Column]),FILTER(Table, Table[ColumnToFilterOn]=EARLIER(Table[Table])))
