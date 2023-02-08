import boto3
from typing import List, Dict

def get_glue_table_schema(glue_client, database_name: str, table_name: str) -> List[Dict[str,str]]: 
    '''
    Returns the schema of the table:table_name in database:database_name. Can be used as the
    dtype parameter to awswrangler.s3.to_parquet

    Paraemeters:
    glue_client: boto3 client to glue.

    Returns:
    List[Dict[str,str]]: where the key is column name and value is the data type
    eg: [{'content_id': 'string'}, {'created_time': 'string'}]
    '''
    response = glue_client.get_table(
        DatabaseName=database_name,
        Name=table_name
    )

    columns = response['Table']['StorageDescriptor']['Columns']

    return [{col["Name"]:col["Type"]} for col in columns]
