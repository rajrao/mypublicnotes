
1. Cast datetime string to integer (take out the cast to date, if its already a date)

        cast(DATE_FORMAT(cast(dateColumn as Date),'YYYYMMdd') as int)
        
       
        Y/YYYY - 2020
        yy/YY - 20
        MM - month 09
        M - month 9
        dd - day
        DD - number of days since start
        hh - 11
        HH - 23
        mm - minute
        ss - seconds
        E - week day name (thu)
        EEEE - week day full name
        W - Week number (4 for 9/24/2019)
        w - week number (39 for 9/24/2019)
        K/KK - same as hh? (11)

      Format uses Java spec: https://docs.oracle.com/javase/7/docs/api/java/text/SimpleDateFormat.html
      Formats: should be one of [“YEAR”, “YYYY”, “YY”, “MON”, “MONTH”, “MM”, “DAY”, “DD”, “HOUR”, “MINUTE”, “SECOND”, “WEEK”, “QUARTER”]

2. Cast string to datetime (where string in this case is formatted as yyyyMMdd

        CAST(UNIX_TIMESTAMP(cast(dateAsStringColumn) , 'yyyyMMdd') AS TIMESTAMP)
 

References:
1. https://docs.databricks.com/spark/latest/spark-sql/language-manual/functions.html#date
1. https://docs.databricks.com/spark/latest/spark-sql/language-manual/index.html
1. https://docs.databricks.com/spark/latest/dataframes-datasets/dates-timestamps.html
