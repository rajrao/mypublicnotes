```
Week of Month =
VAR weekNumType = 1 //1:Sun, 2:Mon
VAR prevMonthLastDay =
    DATE ( YEAR ( 'Date Table'[Date] ), MONTH ( 'Date Table'[Date] ), 1 ) - 1
VAR prevMonthLastWeekCalc =
    WEEKNUM ( prevMonthLastDay, weekNumType )
VAR curWeek =
    WEEKNUM ( 'Date Table'[Date], weekNumType )
RETURN
    IF (
        prevMonthLastWeekCalc > curWeek,
        curWeek,
        curWeek - prevMonthLastWeekCalc + 1
    )
```
