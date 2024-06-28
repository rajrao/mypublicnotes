```sql
CREATE EXTERNAL TABLE `table_name`(
  `column` string COMMENT '', 
  `Qty` double, 
  `col1` boolean,
  `dt_col` timestamp
  )
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.ql.io.parquet.serde.ParquetHiveSerDe' 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.parquet.MapredParquetOutputFormat'
LOCATION
  's3://bucket/folder/folder/'
TBLPROPERTIES (
  'classification'='parquet', 
  'compressionType'='none')
```
