
Convert object/list of objects to json

```python
 print(json.dumps(json.dumps(objs, default = lambda x: x.__dict__)))
```
caveat: wont work for some fields like datetime/date/etc
