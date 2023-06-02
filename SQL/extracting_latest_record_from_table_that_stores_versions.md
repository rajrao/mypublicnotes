Here are some ways to get the latest record from a table that stores every version of a record from a source table.

The metrics and the query execution plan were generated from AWS Athena

**Method 1**

```sql
SELECT count(1) FROM (
SELECT *, ROW_NUMBER() OVER (PARTITION BY id ORDER BY systemmodstamp DESC) rn
FROM source_table
) ordered WHERE rn = 1;
```
|Title||
|-|-|
|Input rows | 257.73 K
|Input bytes | 7.87 MB
|Output rows | 1
|Output bytes | 0.01 KB
|Total runtime | 3.9 seconds

![image](https://github.com/rajrao/mypublicnotes/assets/1643325/30a0f499-c955-4608-a11d-2575909505d7)

**Method 2**
```
select count(1) from (
SELECT * from source_table src
WHERE src.systemmodstamp = 
  (SELECT max(systemmodstamp) 
   FROM source_table maxt 
   WHERE maxt.id = src.id)
)
```
|Title||
|-|-|
|Input rows | 257.73 K
|Input bytes | 7.87 MB
|Output rows| 1
|Output bytes | 0.01 KB
|Total runtime | 4.1 seconds

![image](https://github.com/rajrao/mypublicnotes/assets/1643325/264d5c98-3acd-4d26-baa1-ffad9ab5a532)


**Method 3**

This is here only for demonstrating another method to get the latest record. Though, it has the worst performance.

```
select count(1) from (
SELECT src.* from source_table src
left join source_table as latest 
on src.id=latest.id and latest.systemmodstamp>src.systemmodstamp 
where latest.id is null);
```
|Title||
|-|-|
|Input rows | 515.46 K
|Input bytes | 15.73 MB
|Output rows | 1
|Output bytes | 0.01 KB
|Total runtime | 5.1 seconds

![image](https://github.com/rajrao/mypublicnotes/assets/1643325/2d0282fc-0319-455b-bc61-ef5babd040b5)
