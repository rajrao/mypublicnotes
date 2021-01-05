Instead of using the Expand command (which uses the following command: = Table.ExpandTableColumn(#"Added Custom", "Data", {input columns},{output columns})) *use*

  Manually add a new step and use the following command in it:

        = Table.Combine(#"Added Custom"[Data])
