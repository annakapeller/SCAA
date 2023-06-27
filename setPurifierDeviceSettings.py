import json

def lambda_handler(event, context):
    # Extract payload from the event
    payload = json.loads(event['body'])

    # Extract values from the payload
    fan_rotation_speed = payload['fanRotationSpeed']
    led_light_intensity = payload['LEDLightIntensity']
    device_key_lock = payload['deviceKeyLock']

    # Create the response message
    response_message = f"The following values were set: fanRotationSpeed={fan_rotation_speed}, LEDLightIntensity={led_light_intensity}, deviceKeyLock={device_key_lock}"

    # Construct the response
    response = {
        'statusCode': 200,
        'body': response_message
    }

    return response
