-- Full Name Column (Column on Customer Table)
        
    Full Name = 'Customer'[First Name] & " " & 'Customer'[Last Name]

-- Age Breakdown Calculation (Column on Customer Table)

    Age Breakdown = 
    IF('Customer'[Age] >= 55, "55+",
    IF('Customer'[Age] >= 45, "45-54",
    IF('Customer'[Age] >= 35, "35-44",
    "18-34" ) ) )

-- Month Year
    
    Month Year = FORMAT('Date'[Date], "mm-yyyy")

-- Temperature Key (Column on Internet Sales Table)

    Temperature Key = 
    RELATED('Sales Territory'[Sales Territory Region]) & RELATED('Date'[Month Number Of Year])

-- Total Transactions (Column on Sales Territory table)

    Total Transactions = COUNTROWS(RELATEDTABLE('Internet Sales'))

-- Region Volume

  Region Volume = 
    SWITCH(TRUE(),
        [Total Transactions] >= 7000, "High Volume",
        [Total Transactions] >= 4000, "Medium Volume",
        [Total Transactions] >= 1, "Low Volume",
        "N/A" ) 

***Optional

-- Last Order Date (Column on Customer Table)
  
    Last Order Date = MAXX(RELATEDTABLE('Internet Sales'), 'Internet Sales'[Order Date])

*** Calculated Measures ***

-- Total Transactions (Measure on Internet Sales)

    Total Transactions = COUNTROWS('Internet Sales')

-- Total Sales

    Total Sales = SUM('Internet Sales'[Sales Amount]) 

-- Total Cost

    Total Cost = SUM('Internet Sales'[Total Product Cost])

-- Profit

    Profit = [Total Sales] - [Total Cost]

-- Profit Margin

    Profit Margin = DIVIDE([Profit], [Total Sales])

*** Working with CALCULATE ***

-- Total Sales (All Countries)

  Total Sales (All Countries) = 
  CALCULATE(
      [Total Sales],
      ALL('Sales Territory'[Sales Territory Country] ) ) 

-- Total Sales (All Countries) 

    Total Sales (All Countries) = 
    CALCULATE(
        [Total Sales],
        REMOVEFILTERS('Sales Territory'[Sales Territory Country] ) ) 

-- Remove blanks

-- Total Sales (All Countries)

    Total Sales (All Countries) = 
    IF(
        [Total Sales] = BLANK(),
        BLANK(),
        CALCULATE(
            [Total Sales],
            ALL('Sales Territory'[Sales Territory Country] ) ) )

--Percent of Total

    Country Percent of Total Sales = 
    DIVIDE(
        [Total Sales],
        [Total Sales (All Countries)] )

-- Total Sales (United States)

  Total Sales (United States) = 
    CALCULATE(
        [Total Sales],
        'Sales Territory'[Sales Territory Country] = "United States")

**Remove blanks

-- Total Sales (United States)

    Total Sales (United States) = 
    IF(
        ISBLANK([Total Sales]),
        BLANK(),
        CALCULATE(
            [Total Sales],
            'Sales Territory'[Sales Territory Country] = "United States"))

-- Total Sales (US and Canada) 

    Total Sales (US and Canada) = 
    CALCULATE(
        [Total Sales],
        'Sales Territory'[Sales Territory Country] IN { "United States", "Canada" })

**Optional Method** Sames results as above.

-- Total Sales (US and Canada) 

  Total Sales (US and Canada) = 
    CALCULATE(
        [Total Sales],
        'Sales Territory'[Sales Territory Country] = "United States" || // The double pipe delimiter is an OR condition.
        'Sales Territory'[Sales Territory Country] = "Canada" )

-- Total Sales (2007)

    Total Sales (2007) = 
    CALCULATE(
        [Total Sales],
        'Date'[Year] = 2007)

-- Total Sales (2008)

    Total Sales (2008) = 
    CALCULATE(
        [Total Sales],
        'Date'[Year] = 2008)

**Time Intelligence Calculations**

-- Year to Date Sales

    YTD Sales = 
    TOTALYTD(
        [Total Sales],
        'Date'[Date] )

-- Fiscal Year to Date Sales

    Fiscal YTD Sales = 
    TOTALYTD(
        [Total Sales],
        'Date'[Date],
        "06/30" )

-- Prior Year Sales

    Prior Year Sales = 
    CALCULATE(
        [Total Sales],
        SAMEPERIODLASTYEAR(
            'Date'[Date]  ) )

-- Prior Month Sales

    Prior Month Sales = 
    CALCULATE(
        [Total Sales],
        DATEADD(
            'Date'[Date],
            -1, MONTH ) )

*** Semi Additive Measures ***

    Inventory Balance = 
    SUM('Product Inventory'[Units Balance])


    Closing Balance (Last Date) = 
    CALCULATE(
        [Inventory Balance],
        LASTDATE( 
            'Date'[Date] ) ) 

-- Closing Balance (Non Blank)

    Closing Balance (Non Blank) = 
    CALCULATE(
        [Inventory Balance],
        LASTNONBLANK( 
            'Date'[Date],
            [Inventory Balance] ) ) 

-- Opening Balance Month

    Opening Balance Month = 
    CALCULATE(
        [Inventory Balance],
        LASTNONBLANK( 
            PARALLELPERIOD(
                'Date'[Date],
                -1,
                MONTH),
            [Inventory Balance] ) )

*** Context Transition ***

-- Last Order Date (Column on Customer Table)
    Last Order Date (CT) = 
    CALCULATE(
        MAX('Internet Sales'[Order Date]) 
    )
