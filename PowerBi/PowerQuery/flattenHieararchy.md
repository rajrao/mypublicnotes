An example function to flatten a table with a self referential join that denotes a parent child relationship.

Example:

| Id | Name     | Manager Id | 
|----|----------|------------|
| 1  | Raj      |            | 
| 2  | Batman   | 1          |
| 3  | Superman | 2          |
| 4  | Yoda     | 1          |
| 5  | C3PO     | 4          |
| 6  | R2D2     | 5          |


    let
        flattenedHieararcy = (dataTable as table, keyColumn as text, parentColumn as text)  =>
        let  
            recursiveJoinResultInternal = (FromTable as table, KeyColumn as text, ParentKeyColumn as text, ToTable as table, optional Depth as number) =>
            let
                curDepth = if (Depth=null) then 1 else Depth,
                curKeyColumn = if (Depth=null) then KeyColumn else Number.ToText(curDepth-1) & "." & KeyColumn,
                curParentKeyColumn = Number.ToText(curDepth) & "." & ParentKeyColumn,
                JoinTables = Table.Join(FromTable,{curKeyColumn},
                Table.PrefixColumns(ToTable , Number.ToText(curDepth)),{curParentKeyColumn}, JoinKind.LeftOuter),
                FinalResult = if
                        List.MatchesAll(Table.Column(JoinTables, curParentKeyColumn), each _=null)
                    then FromTable
                    else RecursiveJoinOld(JoinTables, KeyColumn, ParentKeyColumn, ToTable, curDepth+1)
            in
                FinalResult, 
            srcTable = Table.SelectRows(dataTable, each Text.Length(Record.Field(_, parentColumn)) <= 0),
            destTable = Table.SelectRows(dataTable, each Text.Length(Record.Field(_, parentColumn)) > 0),
            Results = recursiveJoinResultInternal(srcTable, keyColumn, parentColumn, destTable)
        in  
            Results
    in
        flattenedHieararcy
        
        
        
| Id | Name | ManagerId | 1.Id | 1.Name | 1.ManagerId | 2.Id | 2.Name   | 2.ManagerId | 3.Id | 3.Name | 3.ManagerId |
|----|------|-----------|------|--------|-------------|------|----------|-------------|------|--------|-------------|
| 1  | Raj  |           | 4    | Yoda   | 1           | 5    | C3PO     | 4           | 6    | R2D2   | 5           |
| 1  | Raj  |           | 2    | Batman | 1           | 3    | Superman | 2           | null | null   | null        |


Reference: https://blog.crossjoin.co.uk/2013/06/22/flattening-a-parentchild-relationship-in-data-explorer/
