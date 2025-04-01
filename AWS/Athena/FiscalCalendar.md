```sql
CREATE EXTERNAL TABLE `fiscal_calendar`(
 `dt` date , 
  `date` string , 
  `year` int , 
  `year_quarter_number` int , 
  `year_quarter` string , 
  `quarter` string , 
  `year_month` string , 
  `year_month_number` string , 
  `month` string , 
  `month_number` int , 
  `day_of_week_number` int , 
  `day_of_week` string , 
  `fiscal_year` string , 
  `fiscal_year_number` int , 
  `fiscal_quarter_number` int , 
  `fiscal_quarter_year` string , 
  `fiscal_year_quarter` string , 
  `fiscal_year_quarter_number` int , 
  `fiscal_month_number` int , 
  `fiscal_month_in_quarter_number` int , 
  `fiscal_week_number` int , 
  `fiscal_week ` string , 
  `day_of_fiscal_year_number` int , 
  `day_of_fiscal_quarter_number` int , 
  `fiscal_month_year` string , 
  `quarter_year` string , 
  `last_day_of_month` boolean , 
  `last_day_of_quarter` boolean
)
ROW FORMAT SERDE 
  'org.apache.hadoop.hive.serde2.OpenCSVSerde' 
WITH SERDEPROPERTIES ( 
  'quoteChar'='\"', 
  'separatorChar'=',') 
STORED AS INPUTFORMAT 
  'org.apache.hadoop.mapred.TextInputFormat' 
OUTPUTFORMAT 
  'org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat'
LOCATION
  's3://xyz/fiscal_calendar/'
TBLPROPERTIES (
  'areColumnsQuoted'='false', 
  'classification'='csv', 
  'columnsOrdered'='true', 
  'compressionType'='none', 
  'customSerde'='OpenCSVSerDe', 
  'delimiter'=',', 
  'objectCount'='1', 
  'skip.header.line.count'='1', 
  'typeOfData'='file')
```
