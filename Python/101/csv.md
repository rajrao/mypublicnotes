
```python
import csv

with io.StringIO(io.BytesIO(data).read().decode("utf-8")) as f_in:
  csv.register_dialect('comma_delimited', delimiter=',', quotechar='"')
  reader = csv.DictReader(f_in)
  for k, row in enumerate(reader, 1):
    for col in row.items():
      print(col)
```

Read data which is in CSV format and manipulate in memory 
```python
f_in = io.StringIO(data)
reader = csv.reader(f_in)
f_out = io.StringIO()
header = [i.replace(' ', '_').replace('(', '').replace(')', '').lower() for i in next(reader)]
f_out.write('\t'.join(header))
f_out.write("\n")

for row in reader:
    r = [i.replace('\\', ' ').replace('\r', ' ').replace('\n', ' ').replace('\t', ' ') for i in row]
    f_out.write('\t'.join(r))
    f_out.write("\n")

f_out.seek(0)
s3 = boto3.client('s3')
print(f_out.getvalue().encode("utf-8"))

f_out.close()
f_in.close()
```

```python
import csv
csv_reader = csv.DictReader(io.StringIO(data), columns)
for csvrow in csv_reader:
  print(csvrow)
  #convert to json
  jsoncontent = jsoncontent + json.dumps(csvrow) + "\n"
```

```python
with io.StringIO(IteratorBytesIO(data).read().decode("utf-8")) as f_in:
  reader = csv.reader(f_in)

  buffer_out = io.StringIO()
  row_count = 0

  for row in reader:
    row_count += 1
    counter = 0
    for r in row:
        counter += 1
        if row_count == 1:
            buffer_out.write(r.lower())
        else:
            buffer_out.write(r.replace('\r', ' ').replace('\n', ' ').replace('\t', ' '))
        if counter != len(row):
            buffer_out.write("\t")
    buffer_out.write("\n")
```
