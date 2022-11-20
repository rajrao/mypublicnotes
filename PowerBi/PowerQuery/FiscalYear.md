Fiscal Year Calculation:

```
Date.Year([date_column]) - (1 * (if Date.Month([date_column]) < 4 then 1 else 0))
```
