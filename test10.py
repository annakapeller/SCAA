import json

def lambda_handler(event, context):
    request_body = json.loads(event['body'])
    key1_value = request_body.get('key1')

    return {
        'statusCode': 200,
        'body': json.dumps(key1_value)
    }
