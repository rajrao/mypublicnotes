Based on: (Create a Date Dimension in Power BI in 4 Steps – Step 1: Calendar Columns)[https://radacad.com/create-a-date-dimension-in-power-bi-in-4-steps-step-1-calendar-columns]


    let
        StartDate = #date(2019,1,1),
        EndDate = #date(2020,12,31),
        NumberOfDays = Duration.Days( EndDate - StartDate ),
        Dates = List.Dates(StartDate, NumberOfDays+1, #duration(1,0,0,0)),
        #"Converted to Table" = Table.FromList(Dates, Splitter.SplitByNothing(), null, null, ExtraValues.Error),
        #"Renamed Columns" = Table.RenameColumns(#"Converted to Table",{{"Column1", "FullDateAlternateKey"}}),
        #"Changed Type" = Table.TransformColumnTypes(#"Renamed Columns",{{"FullDateAlternateKey", type date}}),
        #"Inserted Year" = Table.AddColumn(#"Changed Type", "Year", each Date.Year([FullDateAlternateKey]), type number),
        #"Inserted Month" = Table.AddColumn(#"Inserted Year", "Month", each Date.Month([FullDateAlternateKey]), type number),
        #"Inserted Month Name" = Table.AddColumn(#"Inserted Month", "Month Name", each Date.MonthName([FullDateAlternateKey]), type text),
        #"Inserted Quarter" = Table.AddColumn(#"Inserted Month Name", "Quarter", each Date.QuarterOfYear([FullDateAlternateKey]), type number),
        #"Inserted Week of Year" = Table.AddColumn(#"Inserted Quarter", "Week of Year", each Date.WeekOfYear([FullDateAlternateKey]), type number),
        #"Inserted Week of Month" = Table.AddColumn(#"Inserted Week of Year", "Week of Month", each Date.WeekOfMonth([FullDateAlternateKey]), type number),
        #"Inserted Day" = Table.AddColumn(#"Inserted Week of Month", "Day", each Date.Day([FullDateAlternateKey]), type number),
        #"Inserted Day of Week" = Table.AddColumn(#"Inserted Day", "Day of Week", each Date.DayOfWeek([FullDateAlternateKey]), type number),
        #"Inserted Day of Year" = Table.AddColumn(#"Inserted Day of Week", "Day of Year", each Date.DayOfYear([FullDateAlternateKey]), type number),
        #"Inserted Day Name" = Table.AddColumn(#"Inserted Day of Year", "Day Name", each Date.DayOfWeekName([FullDateAlternateKey]), type text),
        #"Inserted YearWeek" = Table.AddColumn(#"Inserted Day Name", "YearWeek", each [Year]*100+[Week of Year]),
        #"Changed Types" = Table.TransformColumnTypes(#"Inserted YearWeek",{{"Year", Int64.Type}, {"Month", Int64.Type}, {"Quarter", Int64.Type}, {"Week of Year", Int64.Type}, {"Week of Month", Int64.Type}, {"Day", Int64.Type}, {"Day of Week", Int64.Type}, {"Day of Year", Int64.Type},{"YearWeek", Int64.Type}})
    in
        #"Changed Types"
