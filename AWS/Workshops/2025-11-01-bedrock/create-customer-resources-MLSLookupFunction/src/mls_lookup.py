import os

import boto3
import botocore


# Other boto3 clients and variables
boto3_session = boto3.Session(region_name=os.environ['AWS_REGION'])
dynamodb = boto3.resource('dynamodb',region_name=os.environ['AWS_REGION'])

def get_named_parameter(event, name):
    return next(item for item in event['parameters'] if item['name'] == name)['value']

def get_named_property(event, name):
    return next(item for item in event['requestBody']['content']['application/json']['properties'] if item['name'] == name)['value']

def get_mls_listing(event):
    mls_id = get_named_parameter(event, 'mlsId')
    mls_table_name = os.environ['PROPERTY_TABLE_NAME']
    mls_table = dynamodb.Table(mls_table_name)

    try:
        response = mls_table.get_item(
            Key={
                'mls_id': mls_id
            }
        )
        item = response['Item']
    except botocore.exceptions.ClientError as e:
        print(e.response['Error']['Message'])
    except Exception as e:
        print(f"An error occurred: {e}")
        item = "No property was found for the given MLS Id"
    return item

def lambda_handler(event, context):
    response_code = 200
    action_group = event['actionGroup']
    api_path = event['apiPath']
    
    # API path routing
    if api_path == '/mls/{mlsId}/get-property':
        body = get_mls_listing(event)
    else:
        response_code = 400
        body = {"{}::{} is not a valid api, try another one.".format(action_group, api_path)}

    response_body = {
        'application/json': {
            'body': str(body)
        }
    }
    
    # Bedrock action group response format
    action_response = {
        "messageVersion": "1.0",
        "response": {
            'actionGroup': action_group,
            'apiPath': api_path,
            'httpMethod': event['httpMethod'],
            'httpStatusCode': response_code,
            'responseBody': response_body
        }
    }
 
    return action_response