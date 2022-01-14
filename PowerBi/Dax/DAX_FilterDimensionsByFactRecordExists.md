Sometimes you need to filter a slicer that shows data from a dimension so that it shows only those values for which data exists in the facts. A good example of this is when you have a customer dimension, and sales data that spans many years and you have a lot of churn. In that case, your customers list could be very different year over year. 
To implement this, just create a measure that counts the rows in your fact and then use it as a filter on your dimension.

If our examples has Customer as the dimension and Sales Data as the fact and the relationship is setup as:
```
Customer(CustomerId) (1)--->>-----(\*) Sales Data(CustomerId)
```

Then you would create a measure
```
Sales Data Count = CountRows('Sales Data')
```
You would then use "Sales Data Count" as a filter on your customer slicer to show only those where "Sales Data Count" is greater than 0.

Now as you filter based on other dimensions (eg: Calendar), the list of Customers in the slicer will change to show only those with data based on the current set of filters.

Note:

It might be tempting to add a measure called "Sales Data has data":
```
Sales Data has data = CountRows('Sales Data') > 0
```
This does not work, as the filters dont seem to pick up true/false values.

In this case, what I prefer to do is:

```
Sales Data has data = if (CountRows('Sales Data') > 0,1)
```

I then setup the filter has "Sales Data has data" is not blank!

