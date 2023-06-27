import json
import boto3

def lambda_handler(event, context):

    request_body = json.loads(event['body'])
    room_name = request_body['room_name']

    # Create an SNS client with the desired AWS region
    sns = boto3.client('sns', region_name='us-east-1')
    
    try:
        # Publish a message to the SNS topic
        response = sns.publish(
            TopicArn='arn:aws:sns:us-east-1:819662550576:test_queue_topic2',
            Message=room_name
        )
        
        # Return success message and response
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Message published to SNS',
                'SNS response': response
            })
        }
    
    except Exception as e:
        # Return error message
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
