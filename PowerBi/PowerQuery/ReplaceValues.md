Replace value in many columns

    = Table.ReplaceValue(
            #"Promoted Headers", 
            "NA","",
            Replacer.ReplaceValue,
            List.RemoveFirstN(
                Table.ColumnNames(
                  #"Promoted Headers"),
                 4))
