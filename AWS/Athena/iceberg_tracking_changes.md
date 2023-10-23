The following shows how one can use Apache Iceberg to track changes and only update records when there are changes

**Create an iceberg table**
Id is the primary key in this case.

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

**A CTE for source data**
I am using a CTE to simulate source data, you could use anything else. 

note: [murmur3](https://docs.aws.amazon.com/athena/latest/ug/engine-versions-reference-0003.html#:~:text=Binary%20functions-,murmur3,-(binary)%20%E2%80%93%20Computes) is available as part of Athena Engine 3, which is also needed for merge to work. You can also try md5(to_utf8(value1 || value2))

```sql
with cte(id, value1, value2) as
    (
    select 1,'a1','b' union all
    select 4,'morales','mario' union all
    select 2,'c2','d2' 
    )
    select *, murmur3(from_base64(value1 || value2)) as hash from cte
```

**Here is a merge statement that inserts new records and updates only when there are changes**  
The merge statement uses the CTE described above as its source data. You can manipulate the CTE to test various scenarios

```sql
MERGE INTO hash_test as tgt
USING (
    with cte(id, value1, value2) as
    (
    select 1,'a1','b' union all
    select 4,'morales','mario' union all
    select 2,'c2','d2' 
    )
    select *, value1 || value2 as hash from cte
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
