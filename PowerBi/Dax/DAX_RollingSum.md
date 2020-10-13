

	RollingSum = 
	CALCULATE(
		Sum('TableA'[Column To Be Summed])
		FILTER(
			ALLSELECTED('TableA'[ColumnForUseInComputingRollingSum]),
			'TableA'[ColumnForUseInComputingRollingSum] <= MAX('TableA'[ColumnForUseInComputingRollingSum])
		)
	)
