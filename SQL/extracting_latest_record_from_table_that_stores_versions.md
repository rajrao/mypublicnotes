Here are some ways to get the latest record from a table that stores every version of a record from a source table.

The metrics and the query execution plan were generated from AWS Athena. The input table had about 260k rows. The unique output rows were about 130k (about half the records were duplicated).

I prefer Method 1 (one issue it can deal with is if you have multiple records for a given id, with the same systemmodstamp). Method 2 might be more performant and typically can handle really large datasets (especially when you have a lot of different ids and not much duplication). But because of the issue with duplicate systemmodstamp values, I usually go with Method 1.

Finally, I used systemmodstamp. You could use any field (eg: revision_id, etc).

**Method 1**

```sql
SELECT count(1) FROM (
SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY systemmodstamp DESC) rn
FROM source_table
) ordered WHERE rn = 1;
```
|Title|Metric|
|-|-|
|Input rows | 257.73 K
|Input bytes | 7.87 MB
|Output rows | 1
|Output bytes | 0.01 KB
|Total runtime | 3.9 seconds

![image](https://github.com/rajrao/mypublicnotes/assets/1643325/30a0f499-c955-4608-a11d-2575909505d7)

**Method 2**
```sql
select count(1) from (
SELECT * from source_table src
WHERE src.systemmodstamp = 
  (SELECT max(systemmodstamp) 
   FROM source_table maxt 
   WHERE maxt.id = src.id)
)
```
|Title|Metric|
|-|-|
|Input rows | 257.73 K
|Input bytes | 7.87 MB
|Output rows| 1
|Output bytes | 0.01 KB
|Total runtime | 4.1 seconds

![image](https://github.com/rajrao/mypublicnotes/assets/1643325/264d5c98-3acd-4d26-baa1-ffad9ab5a532)


**Method 3**

This is here only for demonstrating another method to get the latest record. Though, it has the worst performance.

```sql
select count(1) from (
SELECT src.* from source_table src
left join source_table as latest 
on src.id=latest.id and latest.systemmodstamp>src.systemmodstamp 
where latest.id is null);
```
|Title|Metric|
|-|-|
|Input rows | 515.46 K
|Input bytes | 15.73 MB
|Output rows | 1
|Output bytes | 0.01 KB
|Total runtime | 5.1 seconds

![image](https://github.com/rajrao/mypublicnotes/assets/1643325/2d0282fc-0319-455b-bc61-ef5babd040b5)


For comparison this is what the following query looked like
```sql
select count(1) from source_table
```
|Title|Metric|
|-|-|
|Input rows|257.73 K|
|Input bytes||
|Output rows|1|
|Output bytes|0.01 KB|
|Total runtime|4.3 seconds|

![image](https://github.com/rajrao/mypublicnotes/assets/1643325/fac35ca8-6df1-4ce2-8b87-930f9e624de1)

