Calculated Column: Returns count of rows that match a certain filtered criterion.


    count = 
    var filter1 = Table[Column1ForFilter]
    var filter2 =Table[Column2ForFilter]
    var countVal = COUNTROWS(
            Filter(
                Table, 
                Table[Column1ForFilter] = filter1
                && Table[Column2ForFilter] = filter2)
        )
    return (if (countVal = BLANK(), 0, countVal))


