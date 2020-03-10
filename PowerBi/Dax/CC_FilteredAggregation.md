    FilteredMaxValue = CALCULATE(MAX(Table[DataColumn]),FILTER(Table, Table[ColumnToFilterOn]=EARLIER(Table[ColumnToFilterOn])))


To find the rows that have above max value:

    IsLatest = Table[FilteredMaxValue]= Confirmed[DataColumn]
