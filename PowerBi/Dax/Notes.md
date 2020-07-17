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

**Time intelligence functions**
   
   https://docs.microsoft.com/en-us/dax/time-intelligence-functions-dax

(DAX Reference)[https://aka.ms/dax]

(Dax.guide)[https://dax.guide/] 
