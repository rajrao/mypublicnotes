zCalendar Table Internal = 
--  
--     Configuration - implemented by RRao - 2022-08-22
--  
VAR __FirstYear = 2001 //YEAR(MIN('Fact Table'[Date_Column])) or YEAR(MIN(MIN('Fact Table'[Date_Column]),MIN('Different Fact Table'[Date_Column])))
VAR __LastYear =  2100 //YEAR(MAX('Fact Table'[Date_Column])) or YEAR(MAX(MAX('Fact Table'[Date_Column]),MAX('Different Fact Table'[Date_Column])))
----------------------------------------
VAR __Calendar = 
    CALENDAR (
        DATE ( __FirstYear, 4, 1 ),
        DATE ( __LastYear, 3, 31) 

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
        VAR __WeekDayNumber = WEEKDAY ( __Date )
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
