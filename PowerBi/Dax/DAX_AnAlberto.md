The Alberto provides a way to filter dimensions in a star-schema without having to create bidirectional associations.

```
The Alberto = INT(not ISEMPTY('Fact Table 1'))
```

or if you have multiple fact tables

```
The Alberto = INT(not ISEMPTY('Fact Table 1') || not ISEMPTY('Fact Table 2'))
```

You use the above measure as a filter on the slicers with the dimension. By doing that, you get a similar behavior as you would get with a bi-directional association, without all the messiness of a bi-directional association.
