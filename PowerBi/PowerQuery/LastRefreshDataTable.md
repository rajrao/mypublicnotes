Useful M code to create a table with one column that contains when the refresh was last run.

```
= #table(type table[LastRefresh=datetime], {{DateTime.LocalNow()}})
```
