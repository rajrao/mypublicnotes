LazySimpleSerDe is the default serde in Athena and used if a SERDE is not specified. The glue crawler uses this as its serde for CSV files and you will typically see these tables defined without a SERDE but just "ROW FORMAT DELIMITED".

**LazySimpleSerDe format does not support quoted fields. To support quoted fields you can use the OpenCSVSerde format.**  

**Recommendation**:  
Use OpenCsvSerde and bring it in as an internal table (eg: _my_table). Expose to end users as a view with cast/try_cast for data-types (eg: my_table).
OpenCsvSerde only supports timestamps (1579059880000) where as LazySimpleSerDe supports customizable formats.


Handling Date and Timestamp with LazySimpleSerDe  
Date and Timestamp have to be formated as yyyy-MM-dd or yyyy-MM-dd HH:mm:ss or yyyy-MM-dd HH:mm:ss.SSS  

**Example LazySimpleSerDe based table for date and timestamps**
```
CREATE EXTERNAL TABLE `test_datettime`(t1 date,  t2 timestamp,  t3 timestamp)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY '\t' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://bucket/folder'
TBLPROPERTIES (
  'areColumnsQuoted'='false', 
  'classification'='csv', 
  'columnsOrdered'='true', 
  'delimiter'='\t', 
  'serialization.null.format'='', 
  'skip.header.line.count'='1', 
  'typeOfData'='file'
  )
```

The above could also be represented as  
```
CREATE EXTERNAL TABLE `test_datettime`(t1 date,  t2 timestamp,  t3 timestamp)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.lazy.LazySimpleSerDe'
WITH SERDEPROPERTIES (
  'field.delim' = ',',
  'escape.delim' = '\\',
  'line.delim' = '\n'
)
LOCATION
  's3://bucket/folder'
TBLPROPERTIES (
  'areColumnsQuoted'='false', 
  'classification'='csv', 
  'columnsOrdered'='true', 
  'skip.header.line.count'='1'
)
```

**Example file**
```
t1	t2 t3
2024-04-25	2024-04-25 13:23:55.123	2024-03-21 15:32:00
```

The LazySimpleSerDe also supports specifying the timestamp format as shown below (done in TBLPROPERTIES)
  
```
'timestamp.formats'='yyyy-MM-dd HH:mm:ss.SSS'
```

In python this would be coded as:

```python
dt.strftime("%Y-%m-%d %H:%M:%S.%f")
```

Here is an example:
```
CREATE EXTERNAL TABLE `table_name`(
  `field1` bigint, 
  `field_2` string, 
  `field_3` string)
ROW FORMAT SERDE 'org.apache.hadoop.hive.serde2.OpenCSVSerde'
WITH SERDEPROPERTIES (
  'separatorChar' = ',',
  'quoteChar' = '"',
  'escapeChar' = '\\',
  'skip.header.line.count' = '1'
)
LOCATION
  's3://bucket_name/folder_name/'
  
  ```
  
  
Somethings to note about OpenCSVSerde SerDe:
 
  1. Timestamps have to be in UNIX numeric TIMESTAMP values (for example, 1579059880000).
  2. If timestamps are stored as "2023-11-01T19:28:40Z", then use a view with the function: **from_iso8601_timestamp** to convert it on the fly.
     if you need to use it in a view then use: cast(from_iso8601_timestamp(column_name) as timestamp) as otherwise you will get an unsupported data type error
  4. Does not support embedded line breaks (you need to escape them to be read correctly).
  5. OpenCSVSerde will read empty fields as empty strings and not as null!
 
See https://docs.aws.amazon.com/athena/latest/ug/csv-serde.html for more info.


**To read as Nulls**  (uses LazySimpleSerDe)  

```
CREATE EXTERNAL TABLE `table_name`(
  `field1` bigint, 
  `field_2` string, 
  `field_3` string)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY ',' 
LOCATION
   's3://bucket_name/folder_name/'
TBLPROPERTIES (
  'serialization.null.format'='')
```
If any field is stored as **,,**, then that field will be read as null. See [AWS](https://docs.aws.amazon.com/redshift/latest/dg/r_CREATE_EXTERNAL_TABLE.html#:~:text=%27serialization.null.format%27%3D%27%20%27)

TblProperties can be updated using an alter statement
```
alter table `table_name` set tblproperties('serialization.null.format'='')
```

The following uses STORED AS INPUTFORMAT as part of the definition and in which case OUTPUTFORMAT has to be also defined

```
CREATE EXTERNAL TABLE `table_name`(
  `field1` bigint, 
  `field_2` string, 
  `field_3` string)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY ',' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://bucket_name/folder_name'
TBLPROPERTIES (
  'areColumnsQuoted'='false', 
  'serialization.null.format'='', 
  'skip.header.line.count'='1')
```

**Useful Infromation**  
https://stackoverflow.com/questions/50723963/how-to-read-quoted-csv-with-null-values-into-amazon-athena: Summary: use OpenCsvSerDe. Bring all fields as strings and cast using try_cast.
