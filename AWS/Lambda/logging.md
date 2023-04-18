The following code is needed to configure the logger to capture log messages
```python
logging.getLogger().setLevel(logging.INFO)
```

An alternative is the following (if you are using Python 3.8 or greater):

```python
import logging
import os

log_level_str = os.environ.get("log_level", "WARNING").upper()
log_level = logging.getLevelName(log_level_str)
if (isinstance(log_level,str)):
    print(f"Invalid log_level {log_level_str}")
    log_level = logging.WARNING
else:
    print(f"logging at level {log_level_str} {log_level}")

#insert code for Python 3.7 here

default_log_args = {
    "level": log_level,
    "format": "%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    "datefmt": "%y-%b-%d %H:%M",
    "force": True,
}
logging.basicConfig(**default_log_args)
_logger = logging.getLogger(__name__)

def lambda_handler(event, context):
    _logger.info("hello info")
    _logger.debug("hello debug")
```

if you are using Python 3.7 or lower you need to use this code in the above code where it says 
**#insert code for Python 3.7 here**

```python
root = logging.getLogger()
if root.handlers:
    for handler in root.handlers:
        root.removeHandler(handler)
```

To configure what level is used, you can setup an environment variable as part of the configuration:
![image](https://user-images.githubusercontent.com/1643325/232924983-fce07eec-3197-4aa1-9119-528304059574.png)
