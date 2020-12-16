**Another sample**

	Delivered Revenue = 

	VAR dateKey =
	    IF (
		HASONEVALUE ( 'Calendar'[Date Key] ),
		SELECTEDVALUE ( 'Calendar'[Date Key] ),
		CALCULATE(MAX('Calendar'[Date Key]),ALL('Revenue'))
	    )
	return 
	    CALCULATE(Sum('Revenue'[Revenue]), All('Calendar'), 'Revenue'[Date Key] <= dateKey)    

**Working 1 (seems just a bit more performant than 2)**

	RollingSum = 
	var maxReportWeekKey = MAX('Revenue'[Report Week Key])
	var reportWeeksToSum = 
	    Filter(
		ALLSELECTED(
		    'Report Week Calendar'
		),
		'Report Week Calendar'[Report Week Key] <= maxReportWeekKey
	    )
	var result =
	    CALCULATE(
		[Revenue], //dax measure: sum('Revenue'[Revenue Change])
		reportWeeksToSum
	    )
	return result

**Working 2**

	////
	RollingSum = 
	CALCULATE(
		[Revenue Change],
		FILTER (
			ALL('Report Week Calendar'),
			'Report Week Calendar'[Report Week Key] <= MAX('Revenue'[Report Week Key])
		)
	)
	

**Method 1** 

This method seems to work the fastest:

	RollingSum = 
	var currentMax =  MAX('TableA'[ColumnForUseInComputingRollingSum]) //eg date key
	return CALCULATE(
	     [Measure containing value to be summed], //eg: Sum('TableA'[ColumnForUseInComputingRollingSum])
	     'TableA'[ColumnForUseInComputingRollingSum] <= currentMax,
	     ALL('TableA'[ColumnForUseInComputingRollingSum])
	)
	

***The following 2 methods likely dont work right*** (timeouts, etc)

**Method 2** 

This method works in more scenarios

	RollingSum = 
	var groupingColumn = SELECTEDVALUE('TableA'[ColumnOverWhichRollingSumShouldBeComputed]) //eg orderid
	var currentMax =  MAX('TableA'[ColumnForUseInComputingRollingSum]) //eg date key
	return CALCULATE(
		Sum('TableA'[ColumnForUseInComputingRollingSum])
		FILTER(
			ALL('TableA'),
			'TableA'[ColumnForUseInComputingRollingSum] <= currentMax && 'TableA'[ColumnOverWhichRollingSumShouldBeComputed] = groupingColumn
		)
	)

**Method 3**

This method works only when 'TableA'\[ColumnForUseInComputingRollingSum] is on the visual

	RollingSum = 
	CALCULATE(
		Sum('TableA'[Column To Be Summed])
		FILTER(
			ALLSELECTED('TableA'[ColumnForUseInComputingRollingSum]), //eg: datekey
			'TableA'[ColumnForUseInComputingRollingSum] <= MAX('TableA'[ColumnForUseInComputingRollingSum])
		)
	)
