**Hive style folders** :  In hive style folders the path has key value pairs  (eg: s3://bucket-name/folder1/folder2/year=2024/month=08/day=13/xxxx.csv)  

In the following case, the projection partitions **do not have to be provided as part of the query** and the data is automatically read.

The below table reads csv files located in folders named dt=2024-04-01, dt=2023-04-01, etc.  
  s3://bucket-name/folder1/folder2/dt=2024-04-01/xxxx.csv  
  s3://bucket-name/folder1/folder2/dt=2023-04-01/xxxx.csv  
Empty fields should be quoted (eg: '')  

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

**Hive style 2**  
  s3://bucket/folder/year=2025/month=12/day=23  
  s3://bucket/folder/year=2026/month=01/day=03

```sql
CREATE EXTERNAL TABLE `deployed_lambda_op_proj2`(
  `title` string, 
  `id` string, 
  `column1` string, 
  `column2` array<struct<key:string,label:string,values:array<string>>> COMMENT 'for a json complex object'
  )
PARTITIONED BY ( 
  `year` int,
  `month` int,
  `day` int
  )
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://bucket/folder/'
TBLPROPERTIES (
  'projection.enabled' = 'true',
  'projection.year.type'  = 'integer',
  'projection.year.range' = '2020,2030',
  'projection.month.type'  = 'integer',
  'projection.month.range' = '1,12',
  'projection.month.digits' = '2',
  'projection.day.type'  = 'integer',
  'projection.day.range' = '1,31',
  'projection.day.digits' = '2',
  'storage.location.template' = 's3://bucket/folder/year=${year}/month=${month}/day=${day}/'
)
```


**Non hive style folders**  : these folders dont have the key name as part of the path.  
eg: s3://bucket-name/folder1/folder2/2024/08/13/xxxx.parquet  

In this case also, **partitions are automatically picked up**!  
```sql
CREATE EXTERNAL TABLE `my_table2`(
  `id` string, 
  `col1` string, 
  `col2` string, 
  `col3` string)
PARTITIONED BY ( 
  `year` string, 
  `month` string, 
  `day` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://bucket-name/folder1/folder2/'
TBLPROPERTIES (
  'classification'='parquet', 
  'projection.enabled'='true')
```



------
In the following example the **partition needs to be provided** as part of where clause (because its type is set as injected)  
eg: ```select * from my_table3 where year = '2024' and month = '08' and 'day' = 13``

s3://bucket-name/folder1/folder2/2024/08/13/USA/xxxx.parquet
```sql
CREATE EXTERNAL TABLE `my_table3`(
  `id` string)
PARTITIONED BY ( 
  `year` string, 
  `month` string, 
  `day` string,
  `country` string
)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://bucket-name/folder1/folder2/'
TBLPROPERTIES (
  'classification'='parquet', 
  'projection.enabled'='true',
  'projection.execution_id.type'='injected', 
  'storage.location.template'='s3://bucket-name/folder1/folder2/${year}/${month}/${day}/${country}/', )
```

The data would be pulled by using a query like
```select * from my_table3 where country='USA'```

**More Examples**

```sql
TBLPROPERTIES (
  'classification'='parquet', 
  'projection.day.format'='yyyy/MM/dd', 
  'projection.day.interval'='1', 
  'projection.day.interval.unit'='DAYS', 
  'projection.day.range'='2021/01/01,NOW', 
  'projection.day.type'='date', 
  'projection.enabled'='true', 
  'storage.location.template'='s3://bucket/folder1/folder2/${day}/'
)
```

```sql
CREATE EXTERNAL TABLE `table1`(
  `id` string, 
  `recordtype` bigint, 
  `creationtime` string
)
PARTITIONED BY ( 
  `year` string, 
  `month` string, 
  `day` string)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://bucket/powerbi_activity_history/'
TBLPROPERTIES (
  'projection.day.digits'='2', 
  'projection.day.range'='1,31', 
  'projection.day.type'='integer', 
  'projection.enabled'='TRUE', 
  'projection.month.digits'='2', 
  'projection.month.range'='1,12', 
  'projection.month.type'='integer', 
  'projection.year.digits'='4', 
  'projection.year.range'='2020,2030', 
  'projection.year.type'='integer')
```

**Fire Hose**
```sql
CREATE EXTERNAL TABLE my_ingested_data (
 ...
)
...
PARTITIONED BY (
 datehour STRING
)
LOCATION "s3://amzn-s3-demo-bucket/prefix/"
TBLPROPERTIES (
 "projection.enabled" = "true",
 "projection.datehour.type" = "date",
 "projection.datehour.format" = "yyyy/MM/dd/HH",
 "projection.datehour.range" = "2024/01/01/00,NOW",
 "projection.datehour.interval" = "1",
 "projection.datehour.interval.unit" = "HOURS",
 "storage.location.template" = "s3://amzn-s3-demo-bucket/prefix/${datehour}/"
)
```

**AWS Connect Logs**
```sql
CREATE EXTERNAL TABLE `amazon_connectlogs`(
  `awsaccountid` string COMMENT 'from deserializer', 
  `agentarn` string COMMENT 'from deserializer', 
  `currentagentsnapshot` struct<agentstatus:struct<arn:string,name:string,starttimestamp:string,type:string>,configuration:struct<agenthierarchygroups:struct<level1:struct<arn:string,name:string>,level2:struct<arn:string,name:string>,level3:struct<arn:string,name:string>,level4:struct<arn:string,name:string>,level5:struct<arn:string,name:string>>,autoaccept:boolean,firstname:string,languagecode:string,lastname:string,proficiencylist:string,routingprofile:struct<arn:string,concurrency:array<struct<availableslots:int,channel:string,maximumslots:int>>,defaultoutboundqueue:struct<arn:string,channels:array<string>,name:string>,inboundqueues:array<struct<arn:string,channels:array<string>,name:string>>,name:string>,sipaddress:string,username:string>,contacts:array<struct<channel:string,connectedtoagenttimestamp:string,contactid:string,initialcontactid:string,initiationmethod:string,queue:struct<arn:string,name:string>,queuetimestamp:string,state:string,statestarttimestamp:string>>,nextagentstatus:struct<arn:string,enqueuedtimestamp:string,name:string,type:string>> COMMENT 'from deserializer', 
  `eventid` string COMMENT 'from deserializer', 
  `eventtimestamp` string COMMENT 'from deserializer', 
  `eventtype` string COMMENT 'from deserializer', 
  `instancearn` string COMMENT 'from deserializer', 
  `previousagentsnapshot` struct<agentstatus:struct<arn:string,name:string,starttimestamp:string,type:string>,configuration:struct<agenthierarchygroups:struct<level1:struct<arn:string,name:string>,level2:struct<arn:string,name:string>,level3:struct<arn:string,name:string>,level4:struct<arn:string,name:string>,level5:struct<arn:string,name:string>>,autoaccept:boolean,firstname:string,languagecode:string,lastname:string,proficiencylist:string,routingprofile:struct<arn:string,concurrency:array<struct<availableslots:int,channel:string,maximumslots:int>>,defaultoutboundqueue:struct<arn:string,channels:array<string>,name:string>,inboundqueues:array<struct<arn:string,channels:array<string>,name:string>>,name:string>,sipaddress:string,username:string>,contacts:array<struct<channel:string,connectedtoagenttimestamp:string,contactid:string,initialcontactid:string,initiationmethod:string,queue:struct<arn:string,name:string>,queuetimestamp:string,state:string,statestarttimestamp:string>>,nextagentstatus:struct<arn:string,enqueuedtimestamp:string,name:string,type:string>> COMMENT 'from deserializer', 
  `version` string COMMENT 'from deserializer')
PARTITIONED BY ( 
  `datehour` string COMMENT '')
ROW FORMAT SERDE 
  'org.openx.data.jsonserde.JsonSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://bucket/amazonconnect/'
TBLPROPERTIES (
  'projection.datehour.format'='yyyy/MM/dd/HH', 
  'projection.datehour.interval'='1', 
  'projection.datehour.interval.unit'='HOURS', 
  'projection.datehour.range'='2024/01/01/00,NOW', 
  'projection.datehour.type'='date', 
  'projection.enabled'='true', 
  'storage.location.template'='s3://bucket/amazonconnect/${datehour}/'
)
```
  


For more info:  
https://docs.aws.amazon.com/athena/latest/ug/partition-projection.html
