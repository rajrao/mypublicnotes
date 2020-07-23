ROUGH - needs to be cleaned up

    Column2 YoY% = 
    VAR __PREV_YEAR =
      CALCULATE(
        SUM('Sheet1'[Column2]),
        DATEADD('Calendar'[FullDateAlternateKey], -1, YEAR)
      )
    RETURN
      DIVIDE(SUM('Sheet1'[Column2]) - __PREV_YEAR, __PREV_YEAR)
  
  
  
  Median of Column2 YoY% = 
VAR __PREV_YEAR =
	CALCULATE(
		MEDIAN('Sheet1'[Column2]),
		DATEADD('Calendar'[FullDateAlternateKey], -1, YEAR)
	)
RETURN
	DIVIDE(MEDIAN('Sheet1'[Column2]) - __PREV_YEAR, __PREV_YEAR)
