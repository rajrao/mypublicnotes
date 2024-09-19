
```sql
CREATE EXTERNAL TABLE `my_table`(
  `id` string COMMENT 'id', 
  `name` string COMMENT 'n', 
  `col1` string COMMENT 'c1', 
  `col2` string COMMENT 'c2')
PARTITIONED BY ( 
  `dt` string COMMENT '')
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
WITH SERDEPROPERTIES ( 
  'separatorChar'=',', 
  'skip.header.line.count'='1') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://bucket-name/folder1/folder2/'
TBLPROPERTIES (
  'classification'='csv', 
  'projection.dt.format'='yyyy-MM-dd', 
  'projection.dt.range'='NOW-3YEARS,NOW+1YEARS', 
  'projection.dt.type'='date', 
  'projection.enabled'='true',
  'serialization.null.format'='')
```
The above table reads csv files located in folders named dt=2024-04-01, dt=2023-04-01, etc.
Empty fields should be quoted (eg: '')
