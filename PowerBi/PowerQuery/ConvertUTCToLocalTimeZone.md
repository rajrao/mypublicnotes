Converts a column called "Time in UTC" to local time

```
= Table.AddColumn(#"Changed Type", "DateTime in Local Zone", each DateTimeZone.ToLocal(DateTime.AddZone([Time in UTC],0)))
```
