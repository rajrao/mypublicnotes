The following are some special cases for implementing RLS where one doesnt have a simple table that can be used with joins/links between the tables that can be used for the security.

**A separate table for access control**

Separate table "**Access**" with a column called "e-mail" and a column that represents data values that user can see and the type of value
|e-mail   |Type   |Name   |
|---|---|---|
|xx@yy.com|Country|USA|
|ab@yy.com|State|Colorado|

The data to be filtered is in a table "**facts**"
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
