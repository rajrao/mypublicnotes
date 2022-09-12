Sample 1

```
let
    Source = ActiveDirectory.Domains("{AD Server Name Here}"),
    corp.hds.com = Source{[Domain="{AD Server Name Here}"]}[#"Object Categories"],
    user1 = corp.hds.com{[Category="user"]}[Objects],
    #"Removed Other Columns" = Table.SelectColumns(user1,{"displayName", "user", "securityPrincipal"}),
    #"Renamed Columns" = Table.RenameColumns(#"Removed Other Columns",{{"displayName", "Display Name"}}),
    #"Expanded user" = Table.ExpandRecordColumn(#"Renamed Columns", "user", {"departmentNumber", "givenName", "mail", "userAccountControl"}, {"Department", "Nick Name", "Mail", "UAC"}),
    #"Expanded securityPrincipal" = Table.ExpandRecordColumn(#"Expanded user", "securityPrincipal", {"sAMAccountName"}, {"Id"}),
    #"Remove disabled user accounts" = Table.SelectRows(#"Expanded securityPrincipal", each ([Mail] <> null and [Mail] <> "") and ([Id] <> null and [Id] <> "") and ([UAC] = 512)),
    #"Lowercased Text" = Table.TransformColumns(#"Remove disabled user accounts",{{"Id", Text.Lower, type text}}),
    #"Extracted Values" = Table.TransformColumns(#"Lowercased Text", {"Department", each if _ <> null then Text.Combine(List.Transform(_, Text.From), ",") else "", type text}),
    #"Remove records without department" = Table.SelectRows(#"Extracted Values", each ([Department] <> "")),
    #"Removed Columns" = Table.RemoveColumns(#"Remove records without department",{"UAC"})
in
    #"Removed Columns"
```
