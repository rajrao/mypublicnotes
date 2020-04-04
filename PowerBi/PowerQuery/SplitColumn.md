1. Use the formula directly: Splitter.SplitTextByAnyDelimiter({">","-"}, QuoteStyle.Csv)    
    Table.SplitColumn(#"Removed Columns", "Column1", Splitter.SplitTextByAnyDelimiter({">","-"}, QuoteStyle.Csv), {"Column1.1", "Column1.2", "Column1.3", "Column1.4", "Column1.5"})
