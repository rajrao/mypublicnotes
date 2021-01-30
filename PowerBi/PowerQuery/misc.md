Remember PowerQuery is a functional language!!!

Null Record

    T = Table.FromRecords({})

Using an if else

    let
        Source = if Text.Lower(#"Parameter1") = "true" then 
                Function.InvokeAfter(()=> #"Table", #duration(0,0,0,5))
            else 
                Table.FromRecords({})
    in
        Source


Functional feature: This code will run only source1 if Parameter1 = S1 and only Source2 if Parameter1 = S2 and both if Parameter = S3.

    let
        start = DateTime.LocalNow(),
        Source1 = Function.InvokeAfter(()=> Table.FromRecords(
            {[X=(Duration.TotalSeconds(DateTime.LocalNow() - start)),start=start,end=DateTime.LocalNow()]},
            type table[X=Decimal.Type,start=DateTimeZone.Type, end=DateTimeZone.Type]
           ), #duration(0,0,0,6)),
        Source2 = Function.InvokeAfter(()=> Table.FromRecords(
            {[X=(Duration.TotalSeconds(DateTime.LocalNow() - start)),start=start,end=DateTime.LocalNow()]},
            type table[X=Decimal.Type,start=DateTimeZone.Type, end=DateTimeZone.Type]
           ), #duration(0,0,0,6)),
        
        result = if Text.Lower(#"Parameter1") = "s1" then
                    Source1
                 else if Text.Lower(#"Parameter1") = "s2" then
                      Source2
                 else if Text.Lower(#"Parameter1") = "s3" then
                    Table.Combine({Source1,Source2})
                 else
                     Table.FromRecords({})
    in
        result
