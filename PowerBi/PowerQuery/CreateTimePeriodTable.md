

```
// Time Period 1
let
    now = DateTimeZone.UtcNow(),
    span = 7, // Days
    begin = now - #duration(0, span, 0, 0),

    year = Date.Year(now),
    month = Date.Month(now),
    day = Date.Day(now),
    hour = Time.Hour(now),

    startingTime = #datetimezone(year, month, day, 0, 0, 0, 0, 0),

    timeList = List.Transform(List.DateTimeZones(startingTime, span, #duration(-1, 0, 0, 0)), each DateTimeZone.ToText(_)),
    timeTable = Table.FromList(timeList, null, {"Timestamp"}),
    extractedDate = Table.TransformColumns(timeTable, {{"Timestamp", each Text.BeforeDelimiter(_, " "), type text}}),
    changedType = Table.TransformColumnTypes(extractedDate,{{"Timestamp", type date}}),
    
    addTimePeriodColumn = Table.AddColumn(changedType, "TimePeriod", each "Last 7 Days"),
    addSortOrderColumn = Table.AddColumn(addTimePeriodColumn, "Sort Order", each "1")
in
    addSortOrderColumn

// Time Period 2
let
    now = DateTimeZone.UtcNow(),
    span = 14, // Days
    begin = now - #duration(0, span, 0, 0),

    year = Date.Year(now),
    month = Date.Month(now),
    day = Date.Day(now),
    hour = Time.Hour(now),

    startingTime = #datetimezone(year, month, day, 0, 0, 0, 0, 0),

    timeList = List.Transform(List.DateTimeZones(startingTime, span, #duration(-1, 0, 0, 0)), each DateTimeZone.ToText(_)),
    timeTable = Table.FromList(timeList, null, {"Timestamp"}),
    extractedDate = Table.TransformColumns(timeTable, {{"Timestamp", each Text.BeforeDelimiter(_, " "), type text}}),
    changedType = Table.TransformColumnTypes(extractedDate,{{"Timestamp", type date}}),
    
    addTimePeriodColumn = Table.AddColumn(changedType, "TimePeriod", each "Last 14 Days"),
    addSortOrderColumn = Table.AddColumn(addTimePeriodColumn, "Sort Order", each "2")
in
    addSortOrderColumn

// Time Period 3
let
    now = DateTimeZone.UtcNow(),
    span = 31, // Days
    begin = now - #duration(0, span, 0, 0),

    year = Date.Year(now),
    month = Date.Month(now),
    day = Date.Day(now),
    hour = Time.Hour(now),

    startingTime = #datetimezone(year, month, day, 0, 0, 0, 0, 0),

    timeList = List.Transform(List.DateTimeZones(startingTime, span, #duration(-1, 0, 0, 0)), each DateTimeZone.ToText(_)),
    timeTable = Table.FromList(timeList, null, {"Timestamp"}),
    extractedDate = Table.TransformColumns(timeTable, {{"Timestamp", each Text.BeforeDelimiter(_, " "), type text}}),
    changedType = Table.TransformColumnTypes(extractedDate,{{"Timestamp", type date}}),
    
    addTimePeriodColumn = Table.AddColumn(changedType, "TimePeriod", each "Last 31 Days"),
    addSortOrderColumn = Table.AddColumn(addTimePeriodColumn, "Sort Order", each "3")
in
    addSortOrderColumn

// Time Period 4
let
    now = DateTimeZone.UtcNow(),
    span = 90, // Days
    begin = now - #duration(0, span, 0, 0),

    year = Date.Year(now),
    month = Date.Month(now),
    day = Date.Day(now),
    hour = Time.Hour(now),

    startingTime = #datetimezone(year, month, day, 0, 0, 0, 0, 0),

    timeList = List.Transform(List.DateTimeZones(startingTime, span, #duration(-1, 0, 0, 0)), each DateTimeZone.ToText(_)),
    timeTable = Table.FromList(timeList, null, {"Timestamp"}),
    extractedDate = Table.TransformColumns(timeTable, {{"Timestamp", each Text.BeforeDelimiter(_, " "), type text}}),
    changedType = Table.TransformColumnTypes(extractedDate,{{"Timestamp", type date}}),
    
    addTimePeriodColumn = Table.AddColumn(changedType, "TimePeriod", each "Last 90 Days"),
    addSortOrderColumn = Table.AddColumn(addTimePeriodColumn, "Sort Order", each "4")
in
    addSortOrderColumn

// Time Period
let
    Source = Table.Combine(
        {
            #"Time Period 1",
            #"Time Period 2",
            #"Time Period 3",
            #"Time Period 4"
        }
    )
in
    Source
```
