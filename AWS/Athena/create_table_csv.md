OpenCSVSerde supports:
1. Gz or Gzip. No additional properties needed.
2. Quoted strings
   

```sql
CREATE EXTERNAL TABLE `tbl_name`(
  `col1` string,
  `col2` double,
)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
WITH SERDEPROPERTIES ( 
  'escapeChar'='\\', 
  'quoteChar'='\"', 
  'separatorChar'=',', 
  'skip.header.line.count'='1') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://bucket/folder/'

```

```
CREATE EXTERNAL TABLE `xyx_csv`(
    col_a string,
    col_b string,
    col_c string
  )
  PARTITIONED BY ( 
  `y` string,
  `m` string)
ROW FORMAT DELIMITED 
  FIELDS TERMINATED BY '\t' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://bucket/path1/y=2025/m=02/'
TBLPROPERTIES (
  'classification'='csv', 
  'delimiter'='\t', 
  'skip.header.line.count'='1', 
  'typeOfData'='file')
```
