import json
import boto3


def lambda_handler(event, context):
    # Extract the SNS message from the event
    sns_message = event['Records'][0]['Sns']['Message']
    
    # Print the message
    print(f"Received message: {sns_message}")
    
     # Create an SNS client with the desired AWS region
    sns = boto3.client('sns', region_name='us-east-1')
    
    # Publish a message to the SNS topic
    response = sns.publish(
        TopicArn='arn:aws:sns:us-east-1:819662550576:test_queue_topic3',
        Message = sns_message
    )
    
    # Check the response
    print(response['MessageId'])
    
    return {
        'statusCode': 200,
        'body': json.dumps('Message printed successfully')
    }
