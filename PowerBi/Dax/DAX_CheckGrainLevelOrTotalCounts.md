In this example, the code returns true if the visual's filter is valid based on some other criterion. In this example, the DataTable's current filters are compared to the filter if all filters were removed and ony the filters from the fields in question are applied.
The countRows example here can be used to return total counts also


    IsBudgetValid :=
    (
        COUNTROWS( DataTable )
    =
        CALCULATE( COUNTROWS( DataTable ),
                   ALL( DataTable ),
                   VALUES( OtherTable1[Column] ),
                   VALUES( OtherTable2[Column] )
        )
    )
