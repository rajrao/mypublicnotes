**Setup S3 bucket:**  
1. Enable Server access logging:  
    1. Log Object Key Format ([DestinationPrefix][SourceAccountId]/​[SourceRegion]/​[SourceBucket]/​[YYYY]/​[MM]/​[DD]/​[YYYY]-[MM]-[DD]-[hh]-[mm]-[ss]-[UniqueString])  
    1. Source of date used in log object key format: S3 event time.

**Log object key example**  
{account-id}/{account-region}/{bucket-name}/​{yyyy}/{mm}/{dd}/{yyyy}-{mm}-{dd}-00-00-00-[UniqueString]


**Setup of Athena Table:**  
[Using Amazon S3 server access logs to identify requests](https://docs.aws.amazon.com/AmazonS3/latest/userguide/using-s3-access-logs-to-identify-requests.html)

Use date-based partitioning:  
```sql
CREATE EXTERNAL TABLE s3_access_logs_db.mybucket_logs( 
 `bucketowner` STRING, 
 `bucket_name` STRING, 
 `requestdatetime` STRING, 
 `remoteip` STRING, 
 `requester` STRING, 
 `requestid` STRING, 
 `operation` STRING, 
 `key` STRING, 
 `request_uri` STRING, 
 `httpstatus` STRING, 
 `errorcode` STRING, 
 `bytessent` BIGINT, 
 `objectsize` BIGINT, 
 `totaltime` STRING, 
 `turnaroundtime` STRING, 
 `referrer` STRING, 
 `useragent` STRING, 
 `versionid` STRING, 
 `hostid` STRING, 
 `sigv` STRING, 
 `ciphersuite` STRING, 
 `authtype` STRING, 
 `endpoint` STRING, 
 `tlsversion` STRING,
 `accesspointarn` STRING,
 `aclrequired` STRING)
 PARTITIONED BY (
   `timestamp` string)
ROW FORMAT SERDE 
 'org.apache.hadoop.hive.serde2.RegexSerDe' 
WITH SERDEPROPERTIES ( 
 'input.regex'='([^ ]*) ([^ ]*) \\[(.*?)\\] ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) (\"[^\"]*\"|-) (-|[0-9]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) (\"[^\"]*\"|-) ([^ ]*)(?: ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*) ([^ ]*))?.*$') 
STORED AS INPUTFORMAT 
 'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
 'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
 's3://bucket-name/prefix-name/account-id/region/source-bucket-name/'
 TBLPROPERTIES (
  'projection.enabled'='true', 
  'projection.timestamp.format'='yyyy/MM/dd', 
  'projection.timestamp.interval'='1', 
  'projection.timestamp.interval.unit'='DAYS', 
  'projection.timestamp.range'='2024/01/01,NOW', 
  'projection.timestamp.type'='date', 
  'storage.location.template'='s3://bucket-name/prefix-name/account-id/region/source-bucket-name/${timestamp}')
```
