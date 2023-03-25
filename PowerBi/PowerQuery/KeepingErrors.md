1. Select keep errors:
![image](https://user-images.githubusercontent.com/1643325/227686191-bef5e7ac-d169-47e1-8133-730f4d4367f0.png)

2. Add a custom column step with Try around the column with error:
![image](https://user-images.githubusercontent.com/1643325/227686391-b1d73576-8665-497b-9555-30b11781c3b2.png)

3. Expand the objects. The key field has the info.

```
#"Kept Errors" = Table.SelectRowsWithErrors(#"Removed Other Columns1", {"Transform File"}),
#"Added Custom" = Table.AddColumn(#"Kept Errors", "Error", each try [Transform File]),
#"Expanded Error" = Table.ExpandRecordColumn(#"Added Custom", "Error", {"HasError", "Error"}, {"HasError", "Error.1"}),
#"Expanded Error.1" = Table.ExpandRecordColumn(#"Expanded Error", "Error.1", {"Reason", "Message", "Detail", "Message.Format", "Message.Parameters"}, {"Reason", "Message", "Detail", "Message.Format", "Message.Parameters"}),
#"Expanded Detail" = Table.ExpandRecordColumn(#"Expanded Error.1", "Detail", {"Key"}, {"Key"}),
#"Expanded Key" = Table.ExpandRecordColumn(#"Expanded Detail", "Key", {"Item", "Kind"}, {"Item", "Kind"})
```
