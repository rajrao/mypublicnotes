This sample function performs similar to a VLookup


    let
        Source = (valueUsedAsSelector as number) => let
            Source = #"Table to Perform Lookup On",
            #"Filtered Rows" = Table.SelectRows(Source, each ([fieldToBeChecked] = valueUsedAsSelector)),
            #"returnValue" = Record.Field(Table.Max( #"Filtered Rows","fieldToBeReturned"),"fieldToBeReturned")  //get a single row and then extract the field as a value
        in
            #"returnValue"
    in
        Source
