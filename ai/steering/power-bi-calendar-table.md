---
inclusion: manual
---

# HV Fiscal Power BI Calendar Table Skill

Create a standardized, enterprise-grade Calendar dimension table in any Power BI semantic model. This skill replicates the proven two-table pattern: a hidden internal calculated table that generates data, and a visible Calendar table that presents it with proper display folders, sort orders, hierarchies, and hidden helper columns.

## Architecture

The calendar uses a **two-table pattern**:
1. **`zCalendar Table Internal`** — hidden DAX calculated table that generates all date intelligence columns
2. **`Calendar`** — visible table referencing the internal table (`= 'zCalendar Table Internal'`), with proper column configuration

## Configuration Parameters

Before creating the calendar, gather these from the user:
- **First Fiscal Month** (default: 4 = April)
- **First Year** (default: derived from fact table min date, or specify explicitly)
- **Last Year** (default: derived from fact table max date, or specify explicitly)
- **First Day of Week** (default: 0 = Sunday; 1 = Monday)
- **Date column** in fact table(s) to link the relationship to

## Step-by-Step Implementation

### Step 1: Create the Internal Calculated Table

Create table `zCalendar Table Internal` with `isHidden: true` using the DAX expression below. Replace the configuration variables at the top as needed:

```dax
VAR __FirstDayOfWeek = 0
VAR __FirstFiscalMonth = 4
VAR __FiscalMonth = 4
VAR __FirstYear = 2022
VAR __LastYear = 2023
VAR __LastMonth = 3
VAR __LastDayOfMonth = 31
VAR __LastFiscalYear = IF(__LastMonth < 4, __LastYear, __LastYear+1)
VAR __LastTransactionDate = Date(__LastYear,12,31)
----------------------------------------
VAR __WeekDayCalculationType = IF ( __FirstDayOfWeek = 0, 7, __FirstDayOfWeek ) + 10
VAR __Calendar =
    CALENDAR (
        DATE ( __FirstYear, __FiscalMonth, 1 ),
        DATE ( __LastFiscalYear, 3, 31)
    )
VAR __Step3 =
    GENERATE (
        __Calendar,
        VAR __UTCTODAY = UTCTODAY()
        VAR __LASTMONTH = EDATE(__UTCTODAY,-1)
        VAR __LASTQTR = EDATE(__UTCTODAY,-3)
        VAR __Date = [Date]
        VAR __YearNumber = YEAR ( __Date )
        VAR __QuarterNumber = QUARTER ( __Date )
        VAR __YearQuarterNumber = CONVERT ( __YearNumber * 4 + __QuarterNumber - 1, INTEGER )
        VAR __MonthNumber = MONTH ( __Date )
        VAR __WeekDayNumber = WEEKDAY ( __Date, __WeekDayCalculationType )
        VAR __WeekDay = FORMAT ( __Date, "ddd" )
        VAR __FiscalYearNumber = __YearNumber - 1 * ( __FirstFiscalMonth > 1 && __MonthNumber < __FirstFiscalMonth )
        VAR __FiscalMonthNumber = __MonthNumber - __FirstFiscalMonth + 1 + 12 * (__MonthNumber < __FirstFiscalMonth)
        VAR __FiscalQuarterNumber = ROUNDUP ( __FiscalMonthNumber / 3, 0 )
        VAR __FiscalYearQuarterNumber = CONVERT ( __FiscalYearNumber * 4 + __FiscalQuarterNumber - 1, INTEGER )
        VAR __FiscalMonthInQuarterNumber = MOD ( __FiscalMonthNumber - 1, 3 ) + 1 + 3 * ( __MonthNumber > 12 )
        VAR __FirstDayOfFiscalYear = DATE(__FiscalYearNumber,__FirstFiscalMonth,1)
        VAR __FirstDayOfFiscalQtr = DATE(__FiscalYearNumber,(__FiscalQuarterNumber-1)*3+__FirstFiscalMonth,1)
        VAR __WeekNum = if (__MonthNumber >= __FirstFiscalMonth, (WEEKNUM(__Date,2) - Weeknum(__FirstDayOfFiscalYear,2) + 1), (Weeknum(Date(__YearNumber,12,31),2) - Weeknum(__FirstDayOfFiscalYear,2)) + WEEKNUM(__Date,2) + 1)
        VAR __CurrentYear = YEAR(__UTCTODAY)
        VAR __CurrentFiscalYear = __CurrentYear - 1 * ( __FirstFiscalMonth > 1 && MONTH ( __UTCTODAY ) < __FirstFiscalMonth )
        VAR __PreviousFiscalYear = __CurrentFiscalYear - 1
        VAR __CurrentFiscalMonthNumber = MONTH(__UTCTODAY) - __FirstFiscalMonth + 1 + 12 * (MONTH(__UTCTODAY) < __FirstFiscalMonth)
        VAR __CurrentFiscalQuarterNumber = ROUNDUP ( __CurrentFiscalMonthNumber / 3, 0 )
        VAR __CurrentFiscalYearQuarterNumber = CONVERT ( __CurrentFiscalYear * 4 + __CurrentFiscalQuarterNumber - 1, INTEGER )
        VAR __PrevFiscalMonthNumber = MONTH(__LASTMONTH) - __FirstFiscalMonth + 1 + 12 * (MONTH(__LASTMONTH) < __FirstFiscalMonth)
        VAR __PrevFiscalQuarterNumber = ROUNDUP ( (MONTH(__LASTQTR) - __FirstFiscalMonth + 1 + 12 * (MONTH(__LASTQTR) < __FirstFiscalMonth)) / 3, 0 )
        VAR __PrevFiscalYearQuarterNumber = CONVERT ( __CurrentFiscalYear * 4 + __PrevFiscalQuarterNumber - 1, INTEGER )
        RETURN ROW (
            "Year", __YearNumber,
            "Year Quarter Number", __YearQuarterNumber,
            "Year Quarter", FORMAT ( __QuarterNumber, "\Q0" ) & "-" & FORMAT ( __YearNumber, "0000" ),
            "Quarter", FORMAT( __QuarterNumber, "\Q0" ),
            "Year Month", FORMAT ( __Date, "mmm yyyy" ),
            "Year Month Number", __YearNumber * 12 + __MonthNumber - 1,
            "Month", FORMAT ( __Date, "mmm" ),
            "Month Number", __MonthNumber,
            "Day of Week Number", __WeekDayNumber,
            "Day of Week", __WeekDay,
            "Fiscal Year", FORMAT ( __FiscalYearNumber, "\F\Y 0000" ),
            "Fiscal Year Number", __FiscalYearNumber,
            "Fiscal Quarter Year", FORMAT ( __FiscalQuarterNumber, "\F\Q0" ) & "-" & FORMAT ( __FiscalYearNumber, "0000" ),
            "Fiscal Year Quarter", FORMAT ( __FiscalYearNumber, "0000" ) & "-" & FORMAT ( __FiscalQuarterNumber, "\F\Q0" ),
            "Fiscal Year Quarter Number", __FiscalYearQuarterNumber,
            "Fiscal Month Number", __FiscalMonthNumber,
            "Fiscal Year Month", FORMAT ( __Date, "mmm" ) & " " & FORMAT ( __FiscalYearNumber, "\F\Y 0000" ),
            "Fiscal Month In Quarter Number", __FiscalMonthInQuarterNumber,
            "Fiscal Quarter", FORMAT( __FiscalQuarterNumber, "\F\Q0" ),
            "Fiscal Week Number", __WeekNum,
            "Fiscal Week ", "FY" & RIGHT(FORMAT(__FiscalYearNumber, "0000"),2) & "-" & FORMAT ( __WeekNum, "00" ),
            "DateWithTransactions", __Date <= __LastTransactionDate,
            "Fiscal Year Type", switch(true(),__FiscalYearNumber = __CurrentFiscalYear, "Current Year", __FiscalYearNumber = __PreviousFiscalYear, "Prev Year", "Other"),
            "Fiscal Quarter Type", switch(true(),__FiscalYearQuarterNumber = __CurrentFiscalYearQuarterNumber, "Current Qtr", __FiscalYearQuarterNumber = __PrevFiscalYearQuarterNumber, "Prev  Qtr", "Other"),
            "Fiscal Month Type", switch(true(),__FiscalYearNumber = __CurrentFiscalYear && __FiscalMonthNumber = __CurrentFiscalMonthNumber, "Current Month", __FiscalYearNumber = __CurrentFiscalYear && __FiscalMonthNumber = __PrevFiscalMonthNumber, "Prev Month", "Other"),
            "Day of Fiscal Year Number", INT(__Date - __FirstDayOfFiscalYear) + 1,
            "Day of Fiscal Quarter Number",INT(__Date - __FirstDayOfFiscalQtr) + 1
        )
    )
RETURN
    __Step3
```

### Step 2: Create the Calendar Presentation Table

Create a calculated table named `Calendar` with:
- `dataCategory: Time`
- DAX expression: `= 'zCalendar Table Internal'`

### Step 3: Configure Column Properties

Apply these settings on the **Calendar** table columns:

#### Display Folders
- **Date:** Date, Day of Week Number, Day of Week, DateWithTransactions, Day of Fiscal Year Number, Day of Fiscal Quarter Number
- **Calendar:** Year, Year Quarter Number, Year Quarter, Quarter, Year Month, Year Month Number, Month, Month Number
- **Fiscal Calendar:** All Fiscal* columns plus Fiscal Year Month

#### Hidden Columns (used for sorting/filtering only)
- Year Quarter Number
- Quarter
- Year Month Number
- Month
- Month Number
- Day of Week Number
- Day of Week
- Fiscal Year Number
- Fiscal Quarter Year
- Fiscal Year Quarter Number
- Fiscal Month Number
- Fiscal Month In Quarter Number
- Fiscal Quarter
- DateWithTransactions
- Day of Fiscal Year Number
- Day of Fiscal Quarter Number

#### Sort By Column Settings
- `Year Month` → sorted by `Year Month Number`
- `Month` → sorted by `Month Number`
- `Day of Week` → sorted by `Day of Week Number`
- `Fiscal Year Month` → sorted by `Year Month Number`

#### Format Strings
- `Date` → `Short Date`
- All integer/number columns → `0`
- `DateWithTransactions` → `"""TRUE""";"""TRUE""";"""FALSE"""`

#### Key Column
- `Date` is the key column (isKey: true)

#### SummarizeBy
- ALL columns set to `summarizeBy: none`

### Step 4: Create Hierarchies

1. **Year Hierarchy:** Year → Year Quarter → Year Month
2. **Fiscal Year Hierarchy:** Fiscal Year → Fiscal Year Quarter → Year Month

### Step 5: Create Relationship

Create a relationship from the fact table's date column to `Calendar[Date]`:
- From: Many side (fact table)
- To: One side (Calendar[Date])
- Cross-filtering: OneDirection

### Step 6: Refresh

Refresh the `zCalendar Table Internal` table, then run a model Calculate refresh.

## MCP Tool Sequence

When implementing via the PowerBI-Modeling-MCP server:

1. `mcp_table_operations` → Create `zCalendar Table Internal` with `daxExpression`, no columns (auto-derived)
2. `mcp_table_operations` → Update: set `isHidden: true`
3. `mcp_table_operations` → Create `Calendar` with `daxExpression: = 'zCalendar Table Internal'`, no columns
4. `mcp_table_operations` → Update Calendar: set `dataCategory: Time`
5. `mcp_batch_column_operations` → BatchUpdate all Calendar columns with displayFolder, isHidden, sortByColumn, formatString, summarizeBy settings
6. `mcp_column_operations` → Update Date column: set `isKey: true`
7. `mcp_user_hierarchy_operations` → Create Year Hierarchy with levels: Year, Year Quarter, Year Month
8. `mcp_user_hierarchy_operations` → Create Fiscal Year Hierarchy with levels: Fiscal Year, Fiscal Year Quarter, Year Month
9. `mcp_relationship_operations` → Create relationship from fact table date column to Calendar[Date]
10. `mcp_table_operations` → Refresh `zCalendar Table Internal` with type Full
11. `mcp_model_operations` → Refresh with type `Calculate`

## Notes

- The DAX uses `UTCTODAY()` for dynamic "Current/Prev" type columns — these update on every refresh
- Fiscal year configuration: change `__FirstFiscalMonth` (4 = April start, FY ends March 31)
- Date range: adjust `__FirstYear` and `__LastYear` to cover your data's full range
- The `DateWithTransactions` column enables filtering visuals to only show dates with actual data
- The internal table is hidden from report authors — they only see the configured Calendar table
- All columns use `summarizeBy: none` to prevent accidental implicit aggregation
- Sort-by columns are hidden to keep the field list clean for report authors
