
1. Cast datetime string to integer (take out the cast to date, if its already a date)

        cast(DATE_FORMAT(cast(dateColumn as Date),'YYYYMMdd') as int)

2. Cast string to datetime (where string in this case is formatted as yyyyMMdd

        CAST(UNIX_TIMESTAMP(cast(dateAsStringColumn) , 'yyyyMMdd') AS TIMESTAMP)
  
 Formats:
 fmt should be one of [“YEAR”, “YYYY”, “YY”, “MON”, “MONTH”, “MM”, “DAY”, “DD”, “HOUR”, “MINUTE”, “SECOND”, “WEEK”, “QUARTER”]


References:
https://docs.databricks.com/spark/latest/spark-sql/language-manual/functions.html#date
https://docs.databricks.com/spark/latest/spark-sql/language-manual/index.html
https://docs.databricks.com/spark/latest/dataframes-datasets/dates-timestamps.html
