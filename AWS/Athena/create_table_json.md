```sql
CREATE EXTERNAL TABLE `unit`(
  `col1` string,
  `col2` double)
PARTITIONED BY ( 
  `dt` string)
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.IgnoreKeyTextOutputFormat'
LOCATION
  's3://bucket/folder/'
TBLPROPERTIES (
  'abc'='some text')
```
