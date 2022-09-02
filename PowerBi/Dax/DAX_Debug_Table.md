```
Debug Table 2 = 
ADDCOLUMNS (
    -- <table> --
    ALL ( 'People'[Email]),
    -- <expression> as name/value pair--
    "Expression Column",
        CALCULATE (
            SUM ( 'People'[Score] )
        ),
    "Expression Column2",
        RANKX(All('People'[Email]),CALCULATE(Sum('People'[Score])))
)

```
