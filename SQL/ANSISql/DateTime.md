
1. Cast datetime string to integer (take out the cast to date, if its already a date)

        cast(DATE_FORMAT(cast(dateColumn as Date),'YYYYMMdd') as int)
  
 
