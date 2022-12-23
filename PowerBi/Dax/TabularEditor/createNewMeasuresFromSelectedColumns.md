
```
//creates a new measure from selected columns
//by replacing "_" with ""

foreach(var c in Selected.Columns)
{
    var newMeasure = c.Table.AddMeasure(
        "M." + c.Name.Replace("_",""),                    // Name
        "SUM(" + c.DaxObjectFullName + ")",    // DAX expression
        c.DisplayFolder                        // Display Folder
    );
    
    // Set the format string on the new measure:
    newMeasure.FormatString = c.FormatString;

    // Provide some documentation:
    newMeasure.Description = "This measure is the sum of column " + c.DaxObjectFullName;

    // Hide the base column:
    c.IsHidden = true;
}
```
