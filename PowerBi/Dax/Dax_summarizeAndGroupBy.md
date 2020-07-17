
## Summarize ##

    R05_SummarizedTable =
    SUMMARIZE (
        'R05_Table',
        R05_Table[Month],
        R05_Table[Weekday],
        "# of days", COUNTROWS ( 'R05_Table' ),
        "First Date", MINX ( 'R05_Table', 'R05_Table'[Value] )
    )


## Group By ##

    R05_Grouped =
    GROUPBY (
        R05_Table,
        R05_Table[Month],
        R05_Table[Weekday],
        "# of days", COUNTX ( CURRENTGROUP (), 'R05_Table'[Value] ),
        "First Date", MINX ( CURRENTGROUP (), 'R05_Table'[Value] )
    )
