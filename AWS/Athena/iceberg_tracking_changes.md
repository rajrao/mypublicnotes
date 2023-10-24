**Change data capture using Athena and iceberg**

Many times in a datalake, you have a source, where the source doesnt provide information about which records changed. Another use case is where you have an ETL, where you have multiple tables and columns taking part in it and its traditionally difficult to track which records changed in that ETL query. This page shows you one method for being able to track those changes and insert only those records that are new or had updates. (at the end, I also show how to track deletes). The method leverages AWS Iceberg tables in Athena (Athena Engine 3) and the upsert mechanism provided via the **merge-into** statement.


TL;DR; Check out the [merge](#Merge) statement used to update only those records that had changes.

**Setup: A CTE for source data**

I am using a CTE to simulate source data, in practice, you would typically use another Athena table as your source, or a query that brings data together from multiple tables (aka ETL), etc.
A key part to this method is using a hashing function that can be used to determine when a record has changes. I use [xxhas64](https://trino.io/docs/current/functions/binary.html#hashing-functions:~:text=of%20binary.-,xxhash64,-(binary))

```sql
with cte(id, value1, value2) as
    (
    select 1,'a1','b' union all
    select 4,'morales','mario' union all
    select 2,'c2','d2' 
    )
    select *, xxhash64(from_base64(value1 || value2)) as hash from cte
```

Note 1: You can use murmur3 instead of xxhash64 using the following code: murmur3(to_utf8(value1 || value2)).

Note 2: Here are the other hashing functions available: https://trino.io/docs/current/functions/binary.html

**Setup: Create an iceberg table**

The iceberg table is your final table. This will track the data that had changes. Id is the primary key in this case, you can have more columns that are part of the primary key used for the update.

```sql
CREATE TABLE
  test_db.hash_test (
  id int,
  value1 string,
  value2 string,
  hash string,
  last_updated_on timestamp)
  LOCATION 's3://my_test_bucket/hash_test'
  TBLPROPERTIES ( 'table_type' ='ICEBERG')
```

**The ##Merge## statement**

Here is a merge statement that inserts new records and updates only when there are changes. The merge statement uses the CTE described above as its source data. You can manipulate the CTE to test various scenarios. The hash column is used to determine when to insert/update data.

```sql
MERGE INTO hash_test as tgt
USING (
    with cte(id, value1, value2, value3) as
    (
    select 1,'a1','b',100 union all
    select 4,'rao','raj',200 union all
    select 2,'c2','d2',300 
    )
    select *, xxhash64(to_utf8(concat_ws('::',coalesce(value1,'-'),coalesce(value2,'-'),coalesce(cast(value3 as varchar))))) as hash from cte
) as src
ON tgt.id = src.id
WHEN MATCHED and src.hash <> tgt.hash
    THEN UPDATE SET  
    value1 = src.value1,
    value2 = src.value2,
    hash = src.hash,
    last_updated_on = current_timestamp
WHEN NOT MATCHED 
THEN INSERT (id, value1, value2, hash, last_updated_on)
      VALUES (src.id, src.value1, src.value2, src.hash, current_timestamp)	  
```

If you need to deal with deletes, you can add as your first matched phrase one of the following options (delete, or archive):
```sql
WHEN MATCHED and src.IsDeleted = 1
  THEN DELETE
```
or 
```sql
WHEN MATCHED and src.IsDeleted = 1
  THEN UPDATE SET  
    is_archived = 1,
    last_updated_on = current_timestamp
```

**Finally some examples of queries to view the data**

```sql
-- see the history of changes
select * from test_db."hash_test$history" order by made_current_at desc

-- use a snasphot_id from above as your value for xxxxx
select * from test_db.hash_test for version as of xxxxx

-- get only the latest records from the table
select * from test_db.hash_test
where last_updated_on in (select max(last_updated_on) from test_db.hash_test)
order by last_updated_on
```

Reference:

1. [Athena Functions](https://docs.aws.amazon.com/athena/latest/ug/functions.html)
2. [Query Delta Lake Tables](https://docs.aws.amazon.com/athena/latest/ug/delta-lake-tables.html)https://docs.aws.amazon.com/athena/latest/ug/delta-lake-tables.html)
3. [Using Apache Iceberg tables](https://docs.aws.amazon.com/athena/latest/ug/querying-iceberg.html)

**Testing Hashing Behavior**

When hashing you need to make sure that null values are handled appropriately.

Ex: null, a, null and a, null, null should be treated as changes. If they generate the same hash, then you will miss this change. Also the hash functions need string input and hence, one needs to cast the data when its not of type string. For this reason, the computation of the hash gets complicated and I have not found a simpler solution around this.

```sql
with cte(id,note, value1, value2,value3) as
(
    select 1,null,'a1','b',1 union all
    select 4,null,'raj','rao',2 union all
    select 5,'both null',null,null,null union all
    select 6,'empty & null','',null,null union all
    select 7,'null & empty',null,'',1 union all
    select 8,'empty-empty','','',2 union all
    select 9,'str-null','a',null,3 union all
    select 10,'null-str',null,'a',4 union all
    select 100,null,'c2','d2',5 
)
select *
,concat_ws('::',coalesce(value1,'-'),coalesce(value2,'-'),coalesce(cast(value3 as varchar)))
, murmur3(to_utf8(concat_ws('::',coalesce(value1,'-'),coalesce(value2,'-'),coalesce(cast(value3 as varchar))))) as hash1
, xxhash64(to_utf8(concat_ws('::',coalesce(value1,'-'),coalesce(value2,'-'),coalesce(cast(value3 as varchar))))) as hash2
from cte
order by id
```

