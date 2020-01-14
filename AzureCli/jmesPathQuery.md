[Jmespath functions](http://jmespath.org/specification.html#built-in-functions)
Below are some basics:

|Command|Notes||
|---|---|---|
|[]|flatten operator||
|[].displayName|flatten operator & return a single property||
|[].[xxx,yyy]|flatten and extract props||
|[].{x:xxxx,y:yyyy}|flatten, extract and rename||
|[n].{x:xxxx}|extract the nth record||
|[n:m].{x:xxxx}|extract records n to m||
|[?contains(displayName, 'searchText')]|return records where display name contains searchText||
|[?starts_with(fieldname,'text')]|returns records where fieldname begins with text||
|$ kvIds=$(az keyvault secret list --vault-name [Name] --query "[].{objectId:id}" --out tsv)|Extract keyvault ids and place in variable||
|sort_by([?starts_with(name,'qa-')].{n:name},&n)|query for starts with and then sort||
|--query "[?name=='UxKeyVaultDev'].{name:name,rg:resourceGroup}"|||
||||
||||
