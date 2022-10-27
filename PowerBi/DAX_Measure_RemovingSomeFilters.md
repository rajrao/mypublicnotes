From: https://www.sqlbi.com/articles/using-allexcept-versus-all-and-values/

Dont use ALLEXCEPT!
_It is common for DAX newbies to forget that ALLEXCEPT, as a CALCULATE modifier, does not introduce new filters. It can only remove existing ones. If there are no filters on Customer[Continent] when ALLEXCEPT is invoked, there will be no filters after ALLEXCEPT has done its job._

**If you want to remove all filters from a table except for some columns**, a safer method is to **rely on the pair REMOVEFILTERS/VALUES**. REMOVEFILTERS (or ALL) removes all the filters from the table; VALUES evaluates the values of a column as visible in the current filter context, and applies the result as a filter:

```
PercOverContinent :=
VAR SelSales = [Sales Amount]
VAR ConSales =
    CALCULATE (
        [Sales Amount],
        REMOVEFILTERS ( 'Customer' ),
        VALUES ( 'Customer'[Continent] )
    )
VAR Result =
    DIVIDE ( SelSales, ConSales )
RETURN
    Result
```

You can use VALUES when you need to retain a filter on a single column. If you need to keep a filter on multiple columns, you can use SUMMARIZE instead of VALUES

```
PercOverState :=
VAR SelSales = [Sales Amount]
VAR StateSales =
    CALCULATE (
        [Sales Amount],
        REMOVEFILTERS ( 'Customer' ),
        SUMMARIZE (
            'Customer',
            'Customer'[Continent],
            'Customer'[Country],
            'Customer'[State]
        )
    )
VAR Result =
    DIVIDE ( SelSales, StateSales )
RETURN
    Result
```
