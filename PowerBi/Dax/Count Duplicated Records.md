If you need to find the number of records that occur more than once as a measure:

```
NumberOfDuplicates = 
var tbl_duplicates = Filter(
    SUMMARIZE('TableA','TableA'[col_1],'TableA'[col_2],
    "CountOfRecords",Count('TableA'[col_1])
    ),
    [CountOfRecords] >= 2
)
return Calculate(CountRows(tbl_duplicates))
```

Notes:
1. SummarizeColumns cannot be used within a measure, so I use Summarize. tbl_duplicates returns a table. This is then filtered to keep only those records where there are more than 1 record. Here I am looking for dups based on col_1 and col_2. If you need only by col_1, then remove the 2nd column.

