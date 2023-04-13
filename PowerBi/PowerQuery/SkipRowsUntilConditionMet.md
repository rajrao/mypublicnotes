Skip rows until Column1 has a "Contract Number"


```
Table.Skip(#"DataSheet",each [Column1] <> "Contract Number")
```
