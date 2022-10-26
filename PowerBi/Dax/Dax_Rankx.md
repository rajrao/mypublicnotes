If RankX returns 1, then make sure you are using All, or AllSelected.

```
Rank = if (HASONEVALUE('Table'[Id]),
  RANKX(All('Table'),calculate(sum('Table'[ranking_column_eg_sales]),,DESC,Dense)
)
```
