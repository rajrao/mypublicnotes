Add the calculated column on the main table.
2 reasons to do this: this will not be filtered. Also, it can be used for slicers.

Count of Children = CALCULATE(COUNTA('ChildTable'[ChildTableColumn]))
