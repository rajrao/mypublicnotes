Here is the simplest way to remove rows from an incoming file until a certain condition is met:

1. Add a step to "Remove Top Rows..." (Remove Rows >> Remove Top Rows)
2. This will add the step 
```= Table.Skip(#"Report Data - 0_Sheet",3)```
3. Change the code to (where **Contract Number** denotes the start of the data)
``` = Table.Skip(Source,each [Column1] <> "Contract Number")```
