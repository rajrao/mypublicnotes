Useful M code to create a table with one column that contains when the refresh was last run.
You can use either one of these code snippets:

**Snippet 1**
```
let

Source = #table(type table[Date Last Refreshed=datetime], {{DateTime.LocalNow()}}),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Date Last Refreshed", type datetime}})

in

#"Changed Type"
```
**Snippet2**
```
let
    Source = #table(type table[#"Data"=text,#"DateTime"=datetimezone], {{"Dataset Last Refreshed at (UTC)",DateTimeZone.FixedUtcNow()}}),
    #"Added Custom" = Table.AddColumn(Source, "Convertor URL", each "https://www.timeanddate.com/worldclock/converter.html?iso=" & DateTimeZone.ToText([DateTime],"yyyymmddThhnn00") & "&p1=1440&p2=176&p3=3818&p4=136&p5=262&p6=tz_myt&p7=248")
in
    #"Added Custom"
```


Please note, that even though the data is stored in DateTimeZone format, there is no way to show this value in the local time zone to the report viewer. Not simply at least. Because PBI.com does not have the functionality to show DTZ in local tz, one needs to keep a table with the userPrincipalName and use it to shift the time. Not ideal at all.

Here is some Dax code to connect it to a time convertor:

```
TimeAndDate Link = "https://www.timeanddate.com/worldclock/converter.html?iso="
    & FORMAT('Last Refresh Info'[Last Refreshed On DateTime Utc],"yyyyMMddTHHmm00")
    & "&p1=1440&p2=tz_pt&p3=tz_mt&p4=136&p5=262&p6=tz_ist&p7=tz_myt&p8=248"

```

**Snipper3** Insert a row into a table with columns named "table_name" and "date time"
```
= Table.InsertRows(Source,0,{[table_name="Dataset", date time=DateTime.LocalNow()]})
```
