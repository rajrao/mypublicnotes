


```
DateAutoTemplate = 
--  
--     Configuration
--  
VAR __FirstDayOfWeek = 0
VAR __FirstFiscalMonth = 4
----------------------------------------
VAR __WeekDayCalculationType = IF ( __FirstDayOfWeek = 0, 7, __FirstDayOfWeek ) + 10
VAR __Calendar = 
    VAR __FirstYear = YEAR ( MINX ( { MIN ( 'Meeting'[CreatedDateTime] ), MIN ( 'Meeting'[End.DateTime] ), MIN ( 'Meeting'[LastModifiedDateTime] ), MIN ( 'Meeting'[Start.DateTime] ), MIN ( 'Meeting'[Start Date] ) }, ''[Value] ) )
    VAR __LastYear =  YEAR ( MAXX ( { MAX ( 'Meeting'[CreatedDateTime] ), MAX ( 'Meeting'[End.DateTime] ), MAX ( 'Meeting'[LastModifiedDateTime] ), MAX ( 'Meeting'[Start.DateTime] ), MAX ( 'Meeting'[Start Date] ) }, ''[Value] ) )
    RETURN CALENDAR (
        DATE ( __FirstYear, 1, 1 ),
        DATE ( __LastYear, 12, 31 )
    )
VAR __Step3 = 
    GENERATE (
        __Calendar,
        VAR __LastTransactionDate = MAXX ( { MAX ( 'Meeting'[CreatedDateTime] ), MAX ( 'Meeting'[End.DateTime] ), MAX ( 'Meeting'[LastModifiedDateTime] ), MAX ( 'Meeting'[Start.DateTime] ), MAX ( 'Meeting'[Start Date] ) }, ''[Value] )
        VAR __Date = [Date]
        VAR __YearNumber = YEAR ( __Date )
        VAR __QuarterNumber = QUARTER ( __Date )
        VAR __YearQuarterNumber = CONVERT ( __YearNumber * 4 + __QuarterNumber - 1, INTEGER )
        VAR __MonthNumber = MONTH ( __Date )
        VAR __WeekDayNumber = WEEKDAY ( __Date, __WeekDayCalculationType )
        VAR __WeekDay = FORMAT ( __Date, "ddd" )
        //VAR __FiscalYearNumber = __YearNumber + 1 * ( __FirstFiscalMonth > 1 && __MonthNumber >= __FirstFiscalMonth )
        VAR __FiscalYearNumber = __YearNumber - 1 * ( __FirstFiscalMonth > 1 && __MonthNumber < __FirstFiscalMonth )
        VAR __FiscalMonthNumber = __MonthNumber - __FirstFiscalMonth + 1 + 12 * (__MonthNumber < __FirstFiscalMonth)
        VAR __FiscalQuarterNumber = ROUNDUP ( __FiscalMonthNumber / 3, 0 )
        VAR __FiscalYearQuarterNumber = CONVERT ( __FiscalYearNumber * 4 + __FiscalQuarterNumber - 1, INTEGER )
        VAR __FirstDayOfFiscalYear = DATE(__FiscalYearNumber,__FirstFiscalMonth,1)
        VAR __WeekNum = CONVERT(((__Date - __FirstDayOfFiscalYear)/7)+1,INTEGER)
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
            "Fiscal Year Quarter", FORMAT ( __FiscalQuarterNumber, "\F\Q0" ) & "-" & FORMAT ( __FiscalYearNumber, "0000" ),
            "Fiscal Year Quarter Number", __FiscalYearQuarterNumber,
            "Fiscal Quarter", FORMAT( __FiscalQuarterNumber, "\F\Q0" ),
            "Fiscal Week Number", __WeekNum,
            "Fiscal Week ", "FY" & RIGHT(FORMAT(__FiscalYearNumber, "0000"),2) & "-" & FORMAT ( __WeekNum, "00" ),
            "DateWithTransactions", __Date <= __LastTransactionDate 
        )
    )
RETURN
    __Step3
```
