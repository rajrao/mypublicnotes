
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

```sql
with timezone as(
 select 
 zone_name,
 from_unixtime(time_start) timestart, 
 from_unixtime(lag(time_start,1) OVER (PARTITION BY zone_name ORDER BY time_start desc)) timeend, 
 abbreviation, gmt_offset, dst  from timezone
)
,sample_times as(
    select cast('2025-03-21 16:00:00.000' as timestamp) utc_sample
    union all
    select cast('2025-02-28 13:00:00.000' as timestamp) utc
)
select zone_name, utc_sample, date_add('second',gmt_offset, utc_sample) utc_sample_to_zone, gmt_offset/3600.0 offset_hours, abbreviation, dst 
from sample_times
join timezone on utc_sample between timestart and timeend
where zone_name = 'America/Los_Angeles'
or zone_name = 'America/Denver'
order by utc_sample, zone_name
```

|zone_name|utc_sample|utc_sample_to_zone|offset_hours|abbreviation|dst|
|--|--|--|--|--|--|
|America/Denver|2025-02-28 13:00:00.000|2025-02-28 06:00:00.000|-7.0|MST|0
|America/Los_Angeles|2025-02-28 13:00:00.000|2025-02-28 05:00:00.000|-8.0|PST|0
|America/Denver|2025-03-21 16:00:00.000|2025-03-21 10:00:00.000|-6.0|MDT|1
|America/Los_Angeles|2025-03-21 16:00:00.000|2025-03-21 09:00:00.000|-7.0|PDT|1

