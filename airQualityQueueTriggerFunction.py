import json
import boto3

def lambda_handler(event, context):
    # Extract the relevant fields from the incoming message
    messages = event['Records']
    
    # Process each message
    for message in messages:
        message_body = message['body']
        
        # Convert the message body from JSON to a Python dictionary
        data = json.loads(message_body)
        
        # Extract the message body
        message_json = data['Message']
    
    message = json.loads(message_json)
    ip_address = message['ip_address']
    attribute = message['attribute']
    value = message['value']
    unit = message['unit']

    # Create the modified message to be published
    modified_message = {
        'ip_address': ip_address,
        'attribute': attribute,
        'value': value,
        'unit': unit
    }

    # Convert the modified message to JSON
    modified_message_json = json.dumps(modified_message)

    # Publish the modified message to the target SNS topic
    sns_client = boto3.client('sns', region_name='us-east-1')
    topic_arn = 'arn:aws:sns:us-east-1:819662550576:airQualityTopic'
    sns_client.publish(
        TopicArn=topic_arn,
        Message=modified_message_json
    )

    return {
        'statusCode': 200,
        'body': 'Message processed and published successfully'
    }
