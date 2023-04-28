
Convert object/list of objects to json

```python
 print(json.dumps(objs, default = lambda x: x.__dict__))
```
caveat: wont work for some fields like datetime/date/etc


Convert badly formatted json string (ie, attributes are not properly quoted with "")"
```python
import re
import json
well_formatted_str = re.sub(r'(?<!\\\\)\'','\"', badly_formatted_str)
data = json.loads(well_formatted_str)
```
