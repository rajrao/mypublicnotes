#https://fabric.guru/comprehensive-date-dimension-table-for-power-bi-datasets-in-fabric
import pandas as pd
import numpy as np
from pandas.tseries.offsets import DateOffset, BMonthEnd
from datetime import datetime

#This is for Microsoft Fabric only to optimize the Delta table
spark.conf.set("spark.microsoft.delta.optimizeWrite.enabled", "true")


def date_dimension(start_date: str, end_date: str) -> pd.DataFrame:

    '''
    Author : Sandeep Pawar | fabric.guru

    This functions creates a date dimension table based on the start date and     end date.     
    start date and end date should be in 'yyyy-mm-dd' format such as '2023-12-31'


    '''

    try:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        end_date = datetime.strptime(end_date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Invalid date format. Please provide dates in 'yyyy-mm-dd' format.")

    if end_date <= start_date:
        raise ValueError("End date should be after start date.")

    df = pd.DataFrame({"Date": pd.date_range(start_date, end_date)})
    df["DateKey"] = df.Date.dt.strftime('%Y%m%d').astype(int)

    today = pd.Timestamp.now().normalize()
    current_week = today.week
    current_month = today.month
    current_quarter = today.quarter
    current_year = today.year

    df["ISODateName"] = df.Date.dt.strftime('%Y-%m-%d')
    df["AmericanDateName"] = df.Date.dt.strftime('%m/%d/%Y')
    df["DayOfWeekName"] = df.Date.dt.day_name()
    df["DayOfWeekShort"] = df.Date.dt.day_name().str[:3]
    df["MonthName"] = df.Date.dt.month_name()
    df["MonthShort"] = df.Date.dt.month_name().str[:3]
    df["YearWeekName"] = df.Date.dt.strftime('%YW%V')
    df["YearMonthName"] = df.Date.dt.strftime('%Y-%m')
    df["MonthYearName"] = df.Date.dt.strftime('%b %Y')
    df["YearQuarterName"] = df.Date.dt.year.astype(str) + 'Q' + df.Date.dt.quarter.astype(str)
    df["Year"] = df.Date.dt.year
    df["YearWeek"] = df.Date.dt.year*100 + df.Date.dt.isocalendar().week
    df["ISOYearWeekCode"] = df.Date.dt.year*100 + df.Date.dt.isocalendar().week
    df["YearMonth"] = df.Date.dt.year*100 + df.Date.dt.month
    df["YearQuarter"] = df.Date.dt.year*100 + df.Date.dt.quarter
    df["DayOfWeekStartingMonday"] = df.Date.dt.dayofweek + 1
    df["DayOfWeek"] = np.where(df.Date.dt.dayofweek == 6, 1, df.Date.dt.dayofweek + 2)
    df["DayOfMonth"] = df.Date.dt.day
    df["DayOfQuarter"] = (df.Date.dt.day - 1) % 91 + 1
    df["DayOfYear"] = df.Date.dt.dayofyear
    df["WeekOfQuarter"] = (df.Date.dt.day - 1) // 7 + 1
    df["WeekOfYear"] = df.Date.dt.isocalendar().week.astype('int64')
    df["ISOWeekOfYear"] = df.Date.dt.isocalendar().week.astype('int64')
    df["Month"] = df.Date.dt.month
    df["MonthOfQuarter"] = (df.Date.dt.month - 1) % 3 + 1
    df["Quarter"] = df.Date.dt.quarter
    df["DaysInMonth"] = df.Date.dt.days_in_month
    df["DaysInQuarter"] = (df.Date + pd.offsets.QuarterEnd(1)).dt.day
    df['DaysInYear'] = df['Date'].dt.is_leap_year+365
    df['FirstDayOfMonthFlag'] = (df['Date'].dt.is_month_start).astype(int)
    df['LastDayOfMonthFlag'] = (df['Date'].dt.is_month_end).astype(int)
    df['IsTodayFlag']=(df['Date'] == pd.Timestamp.today().date()).astype(int)

    df['IsToday'] = np.where(df['Date'] == today, 1, 0)
    df['IsCurrentWeek'] = np.where(df['Date'].dt.isocalendar().week == current_week, 1, 0)
    df['IsCurrentMonth'] = np.where(df['Date'].dt.month == current_month, 1, 0)
    df['IsCurrentYear'] = np.where(df['Date'].dt.year == current_year, 1, 0)
    df['IsCurrentQuarter'] = np.where(df['Date'].dt.quarter == current_quarter, 1, 0)
    df['NextDay'] = df['Date'] + DateOffset(days=1)
    df['PreviousDay'] = df['Date'] - DateOffset(days=1)
    df['PreviousYearDay'] = df['Date'] - DateOffset(years=1)
    df['PreviousMonthDay'] = df['Date'] - DateOffset(months=1)
    df['NextMonthDay'] = df['Date'] + DateOffset(months=1)
    df['NextYearDay'] = df['Date'] + DateOffset(years=1)

    return df

# For testing
start_date = "2023-05-25" 
end_date = "2024-05-25" 

df = date_dimension(start_date, end_date)
df
(spark.createDataFrame(df)
.write
.mode("overwrite")
.format("delta")
.saveAsTable("Date")
)


