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
