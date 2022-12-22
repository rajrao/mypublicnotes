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
  
  
  
  

