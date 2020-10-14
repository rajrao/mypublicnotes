

**Method 1** 

This method works in more scenarios

	RollingSum = 
	var groupingColumn = SELECTEDVALUE('TableA'[ColumnOverWhichRollingSumShouldBeComputed])
	var currentMax =  MAX('TableA'[ColumnForUseInComputingRollingSum])
	return CALCULATE(
		Sum('TableA'[ColumnForUseInComputingRollingSum])
		FILTER(
			ALL('TableA'),
			'TableA'[ColumnForUseInComputingRollingSum] <= currentMax && 'TableA'[ColumnOverWhichRollingSumShouldBeComputed] = groupingColumn
		)
	)

**Method 2**

This method works only when 'TableA'\[ColumnForUseInComputingRollingSum] is on the visual

	RollingSum = 
	CALCULATE(
		Sum('TableA'[Column To Be Summed])
		FILTER(
			ALLSELECTED('TableA'[ColumnForUseInComputingRollingSum]),
			'TableA'[ColumnForUseInComputingRollingSum] <= MAX('TableA'[ColumnForUseInComputingRollingSum])
		)
	)
