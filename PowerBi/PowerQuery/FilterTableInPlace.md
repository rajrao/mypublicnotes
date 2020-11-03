    = Table.SelectRows(Source, each ([ColumnX] = true) and (Date.From(DateTime.FixedLocalNow()) >= [ColumnY] and Date.From(DateTime.FixedLocalNow()) <= [ColumnZ]))
