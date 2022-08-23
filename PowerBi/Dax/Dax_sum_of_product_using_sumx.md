

```
SumOfProduct = 
SumX(TableA, --iterate over ever item in TableA in context
    var lookedUpItem = LOOKUPVALUE('TableB'[ValueColumn],'TableB'[LookupCol1],TableA[LookupCol1],TableB'[LookupCol2],TableA[LookupCol2],)
    return lookedUpItem * TableA[ValueColumn]
)
```
