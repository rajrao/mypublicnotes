   
      MoM % = 
      VAR __PREV_MONTH =
           CALCULATE(
             [MeasureInQuestion],
             DATEADD('Calendar'[FullDateAlternateKey].[Date], -1, MONTH)
           )
         RETURN
           DIVIDE([MeasureInQuestion] - __PREV_MONTH, __PREV_MONTH)
