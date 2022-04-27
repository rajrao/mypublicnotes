Sometimes you need to fix fields where you do not know the name of the inputs before hand. In this case, you could do something complicated with the ETL MetaData Injector, or you could use a scripting technique.
Here are 2 ways:

# User defined Java Class
```java
import java.math.*;
import java.util.*;
import java.util.Map.Entry;


private final HashMap fieldsToUpdate = new HashMap();
private int rowsLeftForGenerateMode = -1;
private int outputRowSize = 0;

public boolean processRow(StepMetaInterface smi, StepDataInterface sdi) throws KettleException {

    // First, get a row from the default input hop
    Object[] r = getRow();

    // If the row object is null, we are done processing.
    if (r == null && !first) {
        setOutputDone();
        return false;
    }
    // If the global "first" flag is true, perform some initialization that can only happen
    // once we have read the first row of input data
    if (first) {
        first = false;

        // Set up the list of fields that will be available after this step
        // Normally, this is simpler, but in the HelloWorld sample, I don't know if
        // there is an input step connected or not.
        if (r == null) {
            rowsLeftForGenerateMode = 100;
        }
        outputRowSize = data.outputRowMeta.size();

        //create a hasmap of the fields keyed by type
        for (int i = 0; i < outputRowSize; i++) {
            ValueMetaInterface valueMeta = data.outputRowMeta.getValueMeta(i);

            String mapKey = valueMeta.getTypeDesc();
            List fieldsForType = (List) fieldsToUpdate.get(mapKey);
            if (fieldsForType == null) {
                fieldsForType = new ArrayList();
                fieldsToUpdate.put(mapKey, fieldsForType);
            }
            fieldsForType.add(valueMeta.getName());
        }
    }
    r = createOutputRow(r, outputRowSize);

    Set entrySet = fieldsToUpdate.entrySet();
    for (Iterator entryIter = entrySet.iterator(); entryIter.hasNext();) {
        Entry entry = (Entry) entryIter.next();
        String fieldType = (String) entry.getKey();
        for (Iterator listIter = ((List) entry.getValue()).iterator(); listIter.hasNext();) {
            String fieldName = (String) listIter.next();
            FieldHelper fieldHelper = get(Fields.Out, fieldName);
            Object data = fieldHelper.getObject(r);
            if ("String".equals(fieldType) && data != null) {
                //data = ((String)data).replaceAll("[\\r\\n\\t]", " ");
                fieldHelper.setValue(r, data);
            }
        }
    }

    // putRow will send the row on to the default output hop.
    putRow(data.outputRowMeta, r);

    // This method will be continuously called until it returns false (i.e. when all rows are processed).
    // Normally, you'd just return true if you are handling input rows or you'd return false when you are done
    // generating new rows.  In this case, we have the below fancy test to figure out when to stop in either case.
    return (rowsLeftForGenerateMode == -1 || rowsLeftForGenerateMode-- > 0);
}

```

# Modified JavaScript value

```javascript
for (var fieldIndx = 0; fieldIndx < getInputRowMeta().size(); fieldIndx++) {
    var valueMeta = getInputRowMeta().getValueMeta(fieldIndx);
    if (valueMeta.getTypeDesc().equals("String")) {
        row[fieldIndx] = replace(replace(replace(row[fieldIndx], "\t", " "), "\n", " "), "\r", " ");
    }
}
```
