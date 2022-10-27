Getting the text value associated to the most recent entry

```
Latest State = 
var most_recent_run_date = CALCULATE(Max('Dag Run'[Start Date Time]),REMOVEFILTERS('Dag Run'),VALUEs('Dag Run'[DAG ID (run)]))
return LOOKUPVALUE('Dag Run'[State],
        'Dag Run'[DAG ID (run)],Max('Dag Run'[DAG ID (run)]),
        'Dag Run'[Start Date Time],most_recent_run_date
    )
```
