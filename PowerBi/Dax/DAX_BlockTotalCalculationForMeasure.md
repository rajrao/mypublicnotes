Use HASONEVALUE when using a measure    
    
    Measure = 
    if (HASONEVALUE('Table1'[Col]), Sum('Table1'[Col]))
