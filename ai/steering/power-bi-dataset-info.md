---
inclusion: manual
---

# Power BI Dataset Info Table Skill

Create a utility table that tracks dataset refresh timestamps and provides timezone conversion links. This table is useful for displaying "Last Refreshed" information on report pages and giving users a quick way to convert the UTC refresh time to their local timezone.

## Purpose

- Records the UTC timestamp of the last data refresh
- Generates a timeanddate.com URL for easy timezone conversion
- Can optionally include the latest date from a fact table for "data as of" reporting

## Table Structure

| Column | Data Type | DataCategory | Description |
|--------|-----------|--------------|-------------|
| Data | String | — | Label describing the row (e.g. "Dataset Last Refreshed at (UTC)") |
| DateTime | DateTime | — | UTC timestamp captured at refresh time |
| Convertor URL | String | WebUrl | Link to timeanddate.com converter pre-filled with the refresh timestamp |

## M Expression (Power Query)

```powerquery
let
    Source = #table(
        type table[#"Data"=text, #"DateTime"=datetimezone],
        {{"Dataset Last Refreshed at (UTC)", DateTimeZone.FixedUtcNow()}}
    ),
    #"Added Custom" = Table.AddColumn(
        Source,
        "Convertor URL",
        each "https://www.timeanddate.com/worldclock/converter.html?iso="
            & DateTimeZone.ToText([DateTime], "yyyymmddThhnn00")
            & "&p1=1440&p2=176&p3=3818&p4=136&p5=262&p6=tz_myt&p7=248"
    )
in
    #"Added Custom"
```

### Customizing Timezone Cities

The URL parameters `p1` through `p7` represent cities on timeanddate.com. Default set:
- p1=1440 (UTC)
- p2=176 (New York)
- p3=3818 (some city)
- p4=136 (London)
- p5=262 (Tokyo)
- p6=tz_myt (Malaysia)
- p7=248 (Sydney)

Replace these with your team's relevant timezones. Find city codes at timeanddate.com.

### Optional: Add Latest Data Date Row

To also track the latest date in your fact table, uncomment and adapt this line in the M expression:

```powerquery
#"PL date" = Table.InsertRows(
    #"Added Custom",
    0,
    {[
        Data = "Data Available Through",
        DateTime = DateTimeZone.From(
            Table.Max(#"YourFactTable", "YourDateColumn")[YourDateColumn]
        )
    ]}
)
```

## Column Properties

- `Data`: summarizeBy = none
- `DateTime`: summarizeBy = none, formatString = "General Date"
- `Convertor URL`: summarizeBy = none, dataCategory = "WebUrl"

Setting `dataCategory: WebUrl` on the Convertor URL column allows Power BI to render it as a clickable hyperlink in table visuals.

## MCP Tool Sequence

When implementing via the PowerBI-Modeling-MCP server:

1. `mcp_table_operations` → Create table `Dataset Info` with:
   - `mExpression`: the Power Query expression above
   - `mode`: Import
   - `columns`: 
     - Data (String, sourceColumn: "Data")
     - DateTime (DateTime, sourceColumn: "DateTime", formatString: "General Date")
     - Convertor URL (String, sourceColumn: "Convertor URL", dataCategory: "WebUrl")
2. `mcp_table_operations` → Refresh with type Full
3. Optionally create a card or table visual on the report showing `[DateTime]` with a title like "Last Refreshed (UTC)"

## Usage in Reports

- Add a **Card visual** bound to `Dataset Info[DateTime]` to show when data was last refreshed
- Add a **Table visual** with `Dataset Info[Data]` and `Dataset Info[Convertor URL]` to give users a clickable timezone converter
- Place these on a hidden "Info" page or in a report tooltip

## Notes

- `DateTimeZone.FixedUtcNow()` captures the exact UTC time when the refresh occurs
- The table refreshes every time the dataset is refreshed — the timestamp is always current
- No relationships needed — this is a standalone utility table
- Keep `summarizeBy: none` on all columns to prevent accidental aggregation
