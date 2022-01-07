
Allows you to pull only partial data in "dev" mode and then in production/regular refresh pull full data. Where data is partitioned into separate dataflows

```
let
   #"allYears" = Table.Combine({#"Dataflow 1"
                                 ,#"Dataflow 2"
                                 ,#"Dataflow 3" 
                                 }),
   #"devYears" = Table.Combine({
                              #"Dataflow 1"
                              }),
   #"data" = if Mode = "dev" 
               then #"devYears" 
               else #"allYears"
in
    #"data"
```
