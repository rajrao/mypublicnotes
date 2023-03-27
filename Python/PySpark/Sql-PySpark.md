from: https://www.linkedin.com/in/mrabhijitsahoo/

|SQL DataType       |    PySpark DataType    |
|-------------------|------------------------|
|INT: for integer values|IntegerType: for integer values|
|BIGINT: for large integer values|LongType: for long integer values|
|FLOAT: for floating point values|FloatType: for floating point values|
|DOUBLE: for double precision floating point values|DoubleType: for double precision floating point values|
|CHAR: for fixed-length character strings|StringType: for character strings|
|VARCHAR: for variable-length character strings|StringType: for character strings|
|DATE: for date values|DateType: for date values|
|TIMESTAMP: for timestamp values|TimestampType: for timestamp values|


**Select**
```sql
SELECT column(s) FROM table
```
```python
df.select("column(s)")
```
```sql
SELECT * FROM table
```
```python
df.select("*")
```

**Distinct**
```sql
SELECT DISTINCT column(s) FROM table
```
```python
df.select("column(s)").distinct()
```
**WHERE**
```sql
SELECT column(s) FROM table WHERE condition
```
```python
df.filter(condition).select("column(s)")
```
**Order By**
```sql
SELECT column(s) FROM table ORDER BY column(s)
```
```python
df.sort("column(s)").select("column(s)")
```
**LIMIT**
```sql
SELECT column(s) FROM table LIMIT n
```
```python
df.limit(n).select("column(s)")
```
**COUNT**
```sql
SELECT COUNT(*) FROM table
```
```python
df.count()
```
**SUM** 
```sql
SELECT SUM(column) FROM table
```
```python
from pyspark.sql.functions import sum;
df.agg(sum("column"))
```
**AVG**
```sql
SELECT AVG(column) FROM table
```
```python
from pyspark.sql.functions import avg;
df.agg(avg("column"))
```
**MAX / MIN**
```sql
SELECT MAX(column) FROM table
```
```python
from pyspark.sql.functions import max;
df.agg(max("column"))
```
**String Length**
```sql
SELECT LEN(string) FROM table
```
```python
from pyspark.sql.functions import length;
df.select(length(col("string")))
```
**Convert to Uppercase, Lowercase**
```sql
SELECT UPPER(string), LOWER(string) FROM table
```
```python
from pyspark.sql.functions import upper;
df.select(upper(col("string")),lower(col("string")))
```
**Concatenate Strings**
```sql
SELECT CONCAT(string1, string2) FROM table
```
```python
from pyspark.sql.functions import concat;
df.select(concat(col("string1"),col("string2")))
```
**Trim String**
```sql
SELECT TRIM(string) FROM table
```
```python
from pyspark.sql.functions import trim;
df.select(trim(col("string")))
```
**Substring**
```sql
SELECT SUBSTRING(string,start, length) FROM table
```
```python
from pyspark.sql.functions import substring;
df.select(substring(col("string"),start, length))
```
**CURDATE,NOW,CURTIME**
```sql
SELECT CURDATE() FROM table
```
```python
from pyspark.sql.functions import current_date;
df.select(current_date())
```
**CAST,CONVERT**
```sql
SELECT CAST(column AS datatype) FROM table
```
```python
df.select(col("column").cast("datatype"))
```
**IF**
```sql
SELECT IF(condition, value1,value2) FROM table
```
```python
from pyspark.sql.functions import when,otherwise;
df.select(when(condition,value1).otherwise(value2))
```
**COALESCE**
```sql 
SELECT COALESCE(column1, column2, column3) FROM table
```
```python
from pyspark.sql.functions import coalesce;
df.select(coalesce("column1","column2","column3"))
```
**JOIN**
```sql
JOIN table1 ON table1.column= table2.column
```
```python
df1.join(df2, "column")
```
**GROUP BY**
```sql
GROUP BY column(s)
```
```python
df.groupBy("column(s)")
```
**PIVOT**
```sql
PIVOT (agg_function(column) FOR pivot_column IN (values))
```
```python
df.groupBy("pivot_column").pivot("column").agg(agg_function)
```

**Logical Operators**
```sql
SELECT column FROM table WHERE column1 = value AND column2 > value
```
```python
df.filter((col("column1") == value) & (col("column2") > value))
```
**IS NULL, IS NOT NULL**
```sql
SELECT column FROM table WHERE column IS NULL
```
```python
df.filter(col("column").isNull()).select("column")
```
**IN**
```
SELECT column FROM table WHERE column IN (value1,value2, value3)
```
```python
df.filter(col("column").isin(value1,value2,value3)).select("column")
```
**LIKE**
```sql
SELECT column FROM table WHERE column LIKE 'value%'
```
```python
df.filter(col("column").like("value%"))
```
**BETWEEN**
```sql
SELECT column FROM table WHERE column
BETWEEN value1 AND value2
```
```python
df.filter((col("column") >= value1) & (col("column") <= value2)).select("column")
```
**UNION, UNION ALL**
```sql
SELECT column FROM table1 
UNION SELECT column FROM table2
```
```python
df1.union(df2).select("column") or df1.unionAll(df2).select("column")
```
**RANK, DENSERANK,ROWNUMBER**
```sql
SELECT column, RANK() OVER(ORDER BY column) as rank FROM table
```
```python
from pyspark.sql import Window;
from pyspark.sql.functions import rank;
df.select("column", rank().over(Window.orderBy("column")).alias("rank"))
```
**CTE**
```sql
WITH cte1 AS (SELECT * FROM table1),
SELECT * FROM cte1 WHERE
condition
```
```python
df.createOrReplaceTempView("cte1");
df_cte1 = spark.sql("SELECT * FROM cte1 WHERE condition");
df_cte1.show() 
```
or 
```python
df.filter(condition1).filter(condition2)
```

**Create Table**
```sql
CREATE TABLE table_name
(column_name data_type constraint);
```
```python
df.write.format("parquet").saveAsTable("table_name")
```
**Create Table with Columns definition**
```sql
CREATE TABLE table_name(column_name data_type [constraints],
column_name data_type [constraints],
...);
```
```python
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DecimalType
schema = StructType([StructField("id", IntegerType(), True),
StructField("name", StringType(), False),
StructField("age", IntegerType(), True),
StructField("salary", DecimalType(10,2), True)])
df = spark.createDataFrame([], schema)
```
**Create Table with Primary Key**
```sql
CREATE TABLE table_name(column_name data_type PRIMARY KEY,...);
```
If table already exists:
```sql
ALTER TABLE table_name ADD PRIMARY KEY (column_name);
```
In PySpark or HiveQL, primary key constraints are not enforced directly.
However, you can use the dropDuplicates() method to remove duplicate rows based on one or more columns.
```python
df = df.dropDuplicates(["id"])
```
**Create Table with Auto Increment constraint**
```sql
CREATE TABLE table_name( id INT AUTO_INCREMENT,
name VARCHAR(255), PRIMARY KEY (id));
```

Not natively supported by the DataFrame API, but there are several ways to achieve the same functionality.
```python
from pyspark.sql.functions import
monotonically_increasing_id
df = df.withColumn("id",
monotonically_increasing_id()+start_value)
```
**Adding a column**
```sql
ALTER TABLE table_name
ADD column_name datatype;
```
```python
from pyspark.sql.functions import lit
df=df.withColumn("column_name",
lit(None).cast("datatype"))
```
**Modifying a column**
```python
ALTER TABLE table_name
MODIFY column_name datatype;
```
```python
df=df.withColumn("column_name", df["column_name"].cast("datatype"))
```
**Dropping a column**
```sql
ALTER TABLE table_name
DROP COLUMN column_name;
```
```python
df = df.drop("column_name")
```
**Rename a column**
```sql
ALTER TABLE table_name
RENAME COLUMN old_column_name TO new_column_name;
```
In mysql,
```sql
ALTER TABLE employees CHANGE COLUMN first_name first_name_new VARCHAR(255);
```
```python
df =df.withColumnRenamed("existing_column","new_column")
```
