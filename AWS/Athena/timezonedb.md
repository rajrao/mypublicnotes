
https://timezonedb.com/download

```sql
CREATE EXTERNAL TABLE `country`(
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
```

```sql  
 CREATE EXTERNAL TABLE `timezone`(
  `zone_name` string,
  `country_code` string,
  `abbreviation` string,
  `time_start` bigint,
  `gmt_offset` int,
  `dst` int
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
Using the table:

```sql
select now(), from_unixtime(to_unixtime(now())-gmt_offset) local_now  from timezone
where zone_name = 'America/Denver' and dst=1
and time_start <= to_unixtime(now())
order by time_start desc
limit 1
```  
```sql
select from_unixtime(time_start), abbreviation, gmt_offset, dst  from timezone
where zone_name = 'America/Denver' and time_start <= to_unixtime(now())
order by time_start desc
limit 1
```
