**Create a calendar table**

    Dates = Calendar (Date(2020,1,1),Today())

**Blank**

    _x = {blank()}

**Create table**

    _t = Datatable( "city", string, "pop", integer,
              {
                   {"A",1},{"B",3}
              }

**Calc**

    _c =
      Var current = col1
      Var prev = calculate(col1, sameperiodlastyear('DimDate'[date]))
       Return (current-prev)/current


**Selected Filters as String**

An interesting property of selected values is that it returns all values when none are selected. This makes it awesome when you are checking if any are selected and if you want to show all if none are selected.

    var selectedvalues = CONCATENATEX(ALLSELECTED('Table'[Column]),'Table'[Column],","))
