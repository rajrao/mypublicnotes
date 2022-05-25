Two ways to print/log exceptions:

```python
import traceback

try:
    1/0
except Exception:
    traceback.print_exc()
```

```python
import logging

try:
    1/0
except Exception:
    logging.exception("An exception was thrown!")
```

**DONOT DO THIS**
As in both of these methods print lines, you will not get stack and line number information.

```python
try:
  1/0
except Exception as ex:
  print(ex)
  print(str(ex))
```


