The glue crawler will use RAW FORM DELIMITED when it encounters a CSV file. But this input format will not support quoted fields. To support quoted fields you can use the OpenCSVSerde format.

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
  
  
Somethings to note about this SerDe:
 
  1. Timestamps have to be in UNIX numeric TIMESTAMP values (for example, 1579059880000)
  2. Does not support embedded line breaks (you need to escape them to be read correctly).
  3. OpenCSVSerde will read empty fields as empty strings and not as null!
 
See https://docs.aws.amazon.com/athena/latest/ug/csv-serde.html for more info.


**To read as Nulls**

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
