
https://docs.aws.amazon.com/athena/latest/ug/show-tables.html
```sql
show tables
```

https://docs.aws.amazon.com/athena/latest/ug/alter-table-set-location.html
```sql
ALTER TABLE tablename SET LOCATION 's3://bucketname/xyz/'
```

show create sql
```sql
SHOW CREATE TABLE table_name
```

Usefult glue-catalog tables that can be used to query athena table metadata: https://docs.aws.amazon.com/athena/latest/ug/querying-glue-catalog.html
