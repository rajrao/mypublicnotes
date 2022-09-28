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
= #table(type table[#"Last Refreshed On DateTime Utc"=datetimezone], {{DateTimeZone.FixedUtcNow()}})
```


Please note, that even though the data is stored in DateTimeZone format, there is no way to show this value in the local time zone to the report viewer. Not simply at least. Because PBI.com does not have the functionality to show DTZ in local tz, one needs to keep a table with the userPrincipalName and use it to shift the time. Not ideal at all.

Here is some Dax code to connect it to a time convertor:

```
TimeAndDate Link = "https://www.timeanddate.com/worldclock/converter.html?iso="
    & FORMAT('Last Refresh Info'[Last Refreshed On DateTime Utc],"yyyymmddThhnn00")
    & "&p1=1440&p2=176&p3=3818&p4=136&p5=262&p6=tz_myt&p7=248"

```
