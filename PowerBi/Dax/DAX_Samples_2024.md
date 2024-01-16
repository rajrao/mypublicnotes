**Return the column that has max based on another column**

```
define 
	measure Fact[MostUsedItem] =
	var filterValue = SELECTEDVALUE(Dimension[ColumnName])
	var columnWithMUI = CALCULATETABLE(SUMMARIZE('Fact','Fact'[MuiColumnName], "Cnt",COUNT('Fact'[MuiColumnName])),FILTER('DimensionTbl',DimensionTable[ColumnName] = FilterValue))
    var top1 = TOPN(1,columnWithMUI, [Cnt], DESC)
	return CALCULATE(MIN('Fact'[MuiColumnName]),top1)

EVALUATE
	SUMMARIZECOLUMNS(Dimension[ColumnName],"MUI",[MostUsedItem])	
	
```

Another calculation that is similar
```
SummarizedTable=CALCULATETABLE(
  SUMMARIZE('TblToSummarize','TblToSummarize'[ColumnToAggregateOn],"CalculatedMin",MIN('TblToSummarize'[ColumnToSummarize])))
 RETURN SUMX(SummarizedTable,[CalculatedMin])
```
