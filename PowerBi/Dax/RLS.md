The following are some special cases for implementing RLS where one **doesnt** have a simple table that can be used with joins/links between the tables that can be used for the security.

**A separate table for access control**

Separate table "**Access**" with a column called "e-mail" and a column that represents data values that user can see and the type of value
|e-mail   |Type   |Name   |
|---|---|---|
|xx@yy.com|Country|USA|
|ab@yy.com|State|Colorado|

The data to be filtered is in a table "**facts**"

**Best Solution** [via StackOverflow](https://stackoverflow.com/a/77813873/44815)
```
var userAccess = 
  SUMMARIZE(
    FILTER('Access', [Email] = USERPRINCIPALNAME()),
    Access[Type], Access[Name]
  )
RETURN
  COUNTROWS(FILTER(userAccess, [Type] = "Country" && [Name] = 'Facts'[Country])) > 0
  ||
  COUNTROWS(FILTER(userAccess, [Type] = "State" && [Name] = 'Facts'[State])) > 0 
```

```
VAR upn = USERPRINCIPALNAME() //xxx@ab.com
VAR security_tbl_country = CALCULATETABLE(
  VALUES('Access'[Name]),
  FILTER(
    'Access',
    'Access'[E-mail] = upn && 'Access'[Type] = "Country"
  )
)
VAR security_tbl_state = CALCULATETABLE(
  VALUES('Access'[Name]),
  FILTER(
    'Access',
    'Access'[E-mail] = upn && 'Access'[Type] = "State"
  )
)
RETURN
  'Facts'[Country] IN security_tbl_country || 'Facts'[State] IN security_tbl_state
```

The above query can be simplified as
```
VAR upn = USERPRINCIPALNAME() //xxx@ab.com
VAR security_tbl = CALCULATETABLE(
  SELECTCOLUMNS('Access','Access'[Name], 'Access'[Type]),
  FILTER(
    'Access',
    'Access'[E-mail] = upn
  )
)
RETURN
  'Facts'[Country] IN SELECTCOLUMNS(FILTER(security_tbl,'Access'[Type] = "Country"),'Access'[Name]) 
   || 'Facts'[State] IN SELECTCOLUMNS(FILTER(security_tbl,'Access'[Type] = "State"),'Access'[Name])
```

**Finally, here is how you can test it via DAX editor**

```
EVALUATE
	
	VAR tbl = CALCULATETABLE(
		'Facts',	// << table you wish to filter using RLS
		FILTER(
			'Facts', // << table you wish to filter using RLS
			//--------------Test your RLS filter below ----------------
			VAR upn = USERPRINCIPALNAME() //xxx@ab.com
			VAR security_tbl = CALCULATETABLE(
			SELECTCOLUMNS('Access',[Name], [Type]),
			FILTER(
				'Access',
				[E-mail] = upn
			)
			)
			RETURN
			'Facts'[Country] IN SELECTCOLUMNS(FILTER(security_tbl,[Type] = "Country"),[Name]) 
			|| 'Facts'[State] IN SELECTCOLUMNS(FILTER(security_tbl,[Type] = "State"),[Name])
		//---------------------------------------------
		)
	)
	RETURN
		tbl
```

Test2:

```
EVALUATE
	
	VAR tbl = CALCULATETABLE(
		'Facts',	// << table you wish to filter using RLS
		FILTER(
			'Facts', // << table you wish to filter using RLS
			//--------------Test your RLS filter below ----------------
			VAR upn = USERPRINCIPALNAME() //xxx@ab.com
			VAR security_tbl = CALCULATETABLE(
			SELECTCOLUMNS('Access','Access'[Name], 'Access'[Type]),
			FILTER(
				'Access',
				'Access'[E-mail] = upn
			)
			)
			RETURN
			'Facts'[Country] IN SELECTCOLUMNS(FILTER(security_tbl,'Access'[Type] = "Country"),'Access'[Name]) 
			|| 'Facts'[State] IN SELECTCOLUMNS(FILTER(security_tbl,'Access'[Type] = "State"),'Access'[Name])
		//---------------------------------------------
		)
	)
	RETURN
		SUMMARIZECOLUMNS(
            		'Facts'[Col1],'Facts'[Col2],
			tbl,
			"Cnt", SUM('Facts'[Col3]),
            		"RC", COUNT('Facts'[Col3])
		)
```
