The JSON serde expects separate json documents in a folder or each json document listed on a separate line (new line).
Often times you get a list of json objects that have to be treated as separate records. The following provides a mechanism to convert a list of objects into a string separated by newlines.


```python
response_as_json = response.json()
filetext = "\n".join([str(d) for d in response_as_json])
```

Sometimes you may need to lowercase the keys:
```python
response_as_json = response.json()
response_as_json = [{k.lower():v for k,v in item.items()} for item in response_as_json]

filetext = "\n".join([str(d) for d in response_as_json])
```
