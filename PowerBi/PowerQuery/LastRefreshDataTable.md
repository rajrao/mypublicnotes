Useful M code to create a table with one column that contains when the refresh was last run.

```
let

Source = #table(type table[Date Last Refreshed=datetime], {{DateTime.LocalNow()}}),
    #"Changed Type" = Table.TransformColumnTypes(Source,{{"Date Last Refreshed", type datetime}})

in

#"Changed Type"
```

```
= #table(type table[#"Last Refreshed On DateTime Utc"=datetimezone], {{DateTimeZone.FixedUtcNow()}})
```


Please note, that even though the data is stored in DateTimeZone format, there is no way to show this value in the local time zone to the report viewer. Not simply at least. Because PBI.com does not have the functionality to show DTZ in local tz, one needs to keep a table with the userPrincipalName and use it to shift the time. Not ideal at all.
