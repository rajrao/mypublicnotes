From: https://community.powerbi.com/t5/Desktop/Convert-json-DateTime-format/m-p/57727/highlight/true#M23595

Converts dates in the format /Date(1648828604825)/ to a Date.

To use it, call it like this 
```
= Table.TransformColumns(#"Expanded Column1",{{"CreatedDateTime", JsonDateToDate, type datetime}})
```

**DateFromJson function**
```
let DateFromJson = (date as any) as any =>
     let
      input = if date is null then "/Date(00000000000000)/"else date,
      Stripped = if Text.StartsWith(input, "/Date(") and Text.EndsWith(input, ")/") then Text.Range(input, 6, Text.Length(input)-8) else error "Not a date",
      Position = Text.PositionOfAny(Stripped, {"+", "-"}, 1),
      Parts = if Position < 0 then { Stripped, "0" } else { Text.Range(Stripped, 0, Position), Text.Range(Stripped, Position) },
      NumberParts = { Number.FromText(Parts{0}), Number.FromText(Parts{1}) },
      Result = Date.FromText("1/1/1970") + #duration(0, 0, 0, (NumberParts{0} + 36000 * NumberParts{1}) / 1000),
      output = if Date.Year(Result) = 1970 then null else Result
     in
  output 
 in DateFromJson
 ```
