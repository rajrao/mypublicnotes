
https://docs.aws.amazon.com/athena/latest/ug/show-tables.html
```sql
show tables
```

https://docs.aws.amazon.com/athena/latest/ug/alter-table-set-location.html
```sql
ALTER TABLE tablename SET LOCATION 's3://bucketname/xyz/'
```

Alter Table add partition
```sql
ALTER TABLE dbname.tablename ADD PARTITION (partition_date='2022-09-22') location 's3://bucket/pathx/2022/09/22/'
```

show create sql
```sql
SHOW CREATE TABLE table_name
```

query data from a certain folder
```sql
select * from account
where regexp_like("$path",'s3://bucket/pathx/pathy/2023/08/10/');
```


Usefult glue-catalog tables that can be used to query athena table metadata: https://docs.aws.amazon.com/athena/latest/ug/querying-glue-catalog.html


**ICEBERG**

Create table
```sql
CREATE TABLE dbname.tablename
WITH (table_type='ICEBERG',
location='s3://bucket/pathx/tablename/',
format='PARQUET',
is_external=false)
AS SELECT
column1, column2, ....
FROM dbname.tablename
;
```

Merge
```sql
MERGE INTO dbname.tablename t USING (
SELECT column1, column2,....
FROM dbname.srctablename
WHERE partition_date ='2022-09-22') s
ON t.id = s.id
WHEN MATCHED AND s.op = 'D' THEN DELETE
WHEN MATCHED THEN
UPDATE SET
column1 = s.column1,
column2 = s.column2,
audit_time_stamp = current_timestamp
WHEN NOT MATCHED THEN
INSERT (column1,column2,audit_time_stamp)
VALUES
(s.column1,s.column2,current_timestamp)
```

timetravel
```sql
SELECT * from dbname.tablename
FOR TIMESTAMP AS OF current_timestamp + interval '-5' minute;
-- FOR TIMESTAMP AS OF TIMESTAMP '2023-08-24 14:31:22.868 UTC'
;

SELECT * from dbname.tablename
FOR VERSION AS OF 2357627428223742678 -- for v.id see: "tablename$history"

```

```sql
select * from "tablename$history" order by made_current_at desc
select * from "tablename$snapshots"
select * from "tablename$refs"
select * from "tablename$manifests"
select * from "tablename$partitions"
select * from "tablename$files"
select content,file_path,file_format,record_count, file_size_in_bytes from "tablename$files"
```

vacuum
```sql
ALTER TABLE dbname.tablename SET TBLPROPERTIES (
'vacuum_min_snapshots_to_keep'='1',
'vacuum_max_snapshot_age_seconds'='1'
)

VACUUM dbname.tablename;
```
