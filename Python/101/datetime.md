
**Midnight**
```python
from datetime import date, datetime, time
midnight_12am = datetime.combine(date.today(), time.min) 
midnight_1159pm = datetime.combine(date.today(), time.max)  
```

**Subtract date**
```python
from_date = to_date - DT.timedelta(days=num_days)
```

**ISO Format**

```python
datetime.today().isoformat()
#output: '2022-06-28T14:30:33.483886'

date.today().isoformat()
#output '2022-06-28'
```
