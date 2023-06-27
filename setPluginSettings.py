import json
import urllib.request

def lambda_handler(event, context):
    # Read payload from the event
    
    payload = json.loads(event['body'])
    
    #payload = event['body']

    # Extract device type and settings from the payload
    device_type = payload['deviceType']
    settings = payload['settings']

    # Define the URL endpoints based on device type
    url = ""
    if device_type == "Purifier":
        url = "https://qhkgpnxtczb5s24wjd5sxngjcm0hofox.lambda-url.us-east-1.on.aws/"

    elif device_type == "Humidifier":
        url = "https://w24yeoz24a7jglqt3xagtcewbi0njsnq.lambda-url.us-east-1.on.aws/"

    # Send the settings payload to the respective URL
    req = urllib.request.Request(url, data=json.dumps(settings).encode('utf-8'), method='POST')
    req.add_header('Content-Type', 'application/json')
    
    with urllib.request.urlopen(req) as response:
        if response.status == 200:
            return {
                'statusCode': 200,
                'body': 'Settings updated successfully'
            }
        else:
            return {
                'statusCode': 500,
                'body': 'Error updating settings'
            }
