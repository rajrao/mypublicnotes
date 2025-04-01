**Useful queries**

https://gist.github.com/sholloway/47cb0d9c641a32a3393f5ec8b6e73bcd

**Search for entities**
```
SELECT Label, QualifiedApiName,  KeyPrefix, NamespacePrefix  from EntityDefinition 
where NamespacePrefix like 'XXX%'
and QualifiedApiName like '%YYY%'
and keyprefix not in ('02c','017','0D5','1CE')
order by qualifiedApiName

```

**Fields on a particular entity**  
```
select Id, EntityDefinition.QualifiedApiName, QualifiedApiName, Description, Label, DataType
from FieldDefinition where EntityDefinition.QualifiedApiName in ('Account')
```

**Referencing related entity fields**  
```
SELECT Name, Account.Name, toLabel(StageName), toLabel(ForecastCategoryName), CloseDate, convertCurrency(Amount), Owner.Alias,
Account.Id, AccountId, Account.RecordTypeId, Owner.Id, OwnerId
FROM Opportunity WHERE 
ORDER BY Account.Name ASC NULLS FIRST, Id ASC NULLS FIRST
```
