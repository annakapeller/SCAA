import json
import boto3

def lambda_handler(event, context):
    # Extract the sensor data from the HTTP request
    request_body = json.loads(event['body'])
    ip_address = request_body['ip_address']
    attribute = request_body['attribute']
    value = request_body['value']
    unit = request_body['unit']

    # Create the sensor data message
    sensor_data_message = {
        'ip_address': ip_address,
        'attribute': attribute,
        'value': value,
        'unit': unit
    }

    # Convert the sensor data message to JSON
    sensor_data_message_json = json.dumps(sensor_data_message)

    # Publish the sensor data message to the appropriate SNS topic
    sns_client = boto3.client('sns', region_name='us-east-1')

    if attribute == 'temperature':
        topic_arn = 'arn:aws:sns:us-east-1:819662550576:temperatureHumidifierTopic'
    elif attribute == 'humidity':
        topic_arn = 'arn:aws:sns:us-east-1:819662550576:humidityHumidifierTopic'
    else:
        return {
            'statusCode': 400,
            'body': f'No topic found for attribute: {attribute}'
        }

    sns_client.publish(
        TopicArn=topic_arn,
        Message=sensor_data_message_json
    )

    return {
        'statusCode': 200,
        'body': 'Sensor data published successfully'
    }