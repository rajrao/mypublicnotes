**Using CSV**

```python
import pandas as pd

data = []
data.append(['a','b','c'])
data.append([1,2,3])
data.append([4,5,6])
df = pd.DataFrame(data, columns=['a','b','c'])
csv_buffer = StringIO()
df.to_csv(csv_buffer, header=False, index=None)
print(csv_buffer.getvalue())
```

**JSON to CSV**

```python
json_data = json.loads(data_as_json)
#or pandas.read_json(json_file_name) if normalization is not needed
normalized_data = pandas.json_normalize(json_data)
normalized_data.to_csv('test.csv', index=False) #index=False will skip output of index
```

reading csv read into a variable called data.
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
#clean up the headers!
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

**Another Example **
```python
  json_body = ''
  csv_body = ''
  with io.StringIO('') as writer:
      csv_writer = csv.writer(writer)
      csv_writer.writerow(['field1', 'field2', 'field3'])
      for ent in entities:
          json_body += json.dumps(ent, default = lambda x: x.__dict__) + '\r\n'
          csv_writer.writerow([ent.field1,ent.field2,ent.field3])
      csv_body = writer.getvalue()
      print(json_body)
      print(csv_body)
```
