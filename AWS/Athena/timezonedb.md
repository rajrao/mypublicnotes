
https://timezonedb.com/download

```sql
CREATE EXTERNAL TABLE `timezone`(
  `country_code` string,
  `country_name` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
WITH SERDEPROPERTIES ( 
  'escapeChar'='\\', 
  'quoteChar'='\"', 
  'separatorChar'=',', 
  'skip.header.line.count'='0') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://xxxx/ent/timezonedb/country/'
  
  
 CREATE EXTERNAL TABLE `timezone`(
  `zone_name` string,
  `country_code` string,
  `abbreviation` string,
  `time_start` int,
  `gmt_offset` int,
  `dst` boolean
  )
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
WITH SERDEPROPERTIES ( 
  'escapeChar'='\\', 
  'quoteChar'='\"', 
  'separatorChar'=',', 
  'skip.header.line.count'='0') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://xxxx/ent/timezonedb/timezone/'
```
