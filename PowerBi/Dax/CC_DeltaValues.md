Needs implementation of GroupedIndex in PowerQuery (see: [GroupedIndex](https://github.com/rajrao/mypublicnotes/blob/master/PowerBi/PowerQuery/GroupedIndex.md))

    DeltaValue = 
    var curIndex = Table[GroupIndex]
    var prevIndex = curIndex-1
    var curFilteredValue = Table[ColumnToFilterOn]

    return Table[ValueColumn] - CALCULATE(Max(Table[ValueColumn]),
                                  FILTER(All(Table), 
                                          Table[GroupIndex] = prevIndex && Table[ColumnToFilterOn] = curFilteredValue)
                                        )
