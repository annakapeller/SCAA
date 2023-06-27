import json
import boto3

def lambda_handler(event, context):

    # Create an SNS client with the desired AWS region
    sns = boto3.client('sns', region_name='us-east-1')
    
    records = json.dumps(event['Records'])
    
    # Publish a message to the SNS topic
    response = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:819662550576:test_queue_topic3',
        Message = records
    )
    
    # Check the response
    print(response['MessageId'])

    
    return {
        'statusCode': 200,
        'body': json.dumps(response)
    }