
```python
import boto3

athena = boto3.client('athena')

def get_table_schema(database, table):
    query = f"DESCRIBE {database}.{table}"
    response = athena.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': 's3://my-bucket/athena/results/'
        }
    )

    execution_id = response['QueryExecutionId']
    result = athena.get_query_results(
        QueryExecutionId=execution_id,
        MaxResults=1000
    )

    schema = []
    for row in result['ResultSet']['Rows'][1:]:
        column = row['Data'][0]['VarCharValue']
        data_type = row['Data'][1]['VarCharValue']
        schema.append((column, data_type))

    return schema

schema = get_table_schema("my_database", "my_table")
print(schema)

```
