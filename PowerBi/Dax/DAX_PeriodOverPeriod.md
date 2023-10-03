```
%Change MoM% =
VAR __PREV_PERIOD = CALCULATE([MeasureInQuestion], DATEADD('Calendar'[Date], -1, MONTH))
RETURN
    if ([MeasureInQuestion] <> blank(),DIVIDE([MeasureInQuestion] - __PREV_PERIOD , __PREV_PERIOD ))
```

```
%Change YoY% =
VAR __PREV_PERIOD = CALCULATE([MeasureInQuestion], DATEADD('Calendar'[Date], -1, QUARTER))
RETURN
    if ([MeasureInQuestion] <> blank(),DIVIDE([MeasureInQuestion] - __PREV_PERIOD , __PREV_PERIOD ))
```          
