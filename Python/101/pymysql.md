
**using parameters in execute or execute_mani**

https://pymysql.readthedocs.io/en/latest/modules/cursors.html#pymysql.cursors.Cursor.execute

https://github.com/PyMySQL/mysqlclient/blob/main/MySQLdb/cursors.py#L171


```python
update_statement = "UPDATE object set Column1 = '%(column1Value)s' where keyColumn = %(keyValue)s;"
args = {'column1Value': 'Hello World', 'object_id':1234 }
cur.execute(update_statement, args)
```
